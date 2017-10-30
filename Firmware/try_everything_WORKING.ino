
//Queues, handshake, semaphore, acknowledge working, structure, resend, serializing works, scheduling can be improved but okay for nw
#include <Arduino_FreeRTOS.h>
#include <task.h>
#include <queue.h>
#include <semphr.h>

void establishContact();
QueueHandle_t xQueue0;
SemaphoreHandle_t xMutexSemaphore = NULL;
SemaphoreHandle_t xBinarySemaphore;
TickType_t prevWakeTimeRead;
TickType_t prevWakeTimeSend;

const int xpin0 = A3;
const int ypin0 = A4;
const int zpin0 = A5;

// the setup function runs once when you press reset or power the board
void setup() {

  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  Serial.println("Start up");
  establishContact();
  //Serial.println("Finish contact");
  xTaskCreate(TaskR, "TaskR", 2000, NULL, 2, NULL);
  xTaskCreate(Accel0, "Accel0", 2500, NULL, 2, NULL);
  xQueue0 = xQueueCreate(36, sizeof(int));
  xMutexSemaphore = xSemaphoreCreateMutex();
  xBinarySemaphore = xSemaphoreCreateBinary();
  xSemaphoreGive(xBinarySemaphore);
}

void loop()
{
}

void TaskR(void *pvParameters)
{
  float x0 = 0;
  float y0 = 0;
  float z0 = 0;
  int x0Int, y0Int, z0Int;
  prevWakeTimeRead = xTaskGetTickCount();
  while (1)
  {
    if (xSemaphoreTake(xBinarySemaphore, 10)) {
      if (xSemaphoreTake(xMutexSemaphore, 10)) {
        Serial.println("read");
        x0 = analogRead(xpin0);
        y0 = analogRead(ypin0);
        z0 = analogRead(zpin0);

        //Convert float to int
        x0Int = x0 * 100;
        y0Int = y0 * 100;
        z0Int = z0 * 100;
        
        xQueueSendToBack(xQueue0, &x0Int, 10);
        xQueueSendToBack(xQueue0, &y0Int, 10);
        xQueueSendToBack(xQueue0, &z0Int, 10);

        xSemaphoreGive(xMutexSemaphore);
      }
    }
  }
  vTaskDelayUntil(&prevWakeTimeSend, 300);
}

void Accel0(void *pvParameters)
{
  int readByte = 0;
  int x0Rx, y0Rx, z0Rx;
  char x0Char[5], y0Char[5], z0Char[5];
  int frameNum = 0;
  char frameNumChar[4];
  char messageStr[256];
  unsigned int len;
  int sendFlag = 0;
  int counter = 0;
  char checkSum = 0;

  prevWakeTimeSend = xTaskGetTickCount();
  while (1)
  {
    if (xSemaphoreTake(xMutexSemaphore, 10)) {
      if (Serial.available()) {
        readByte = Serial.read();
      }
      if (readByte == 'A') {
        sendFlag = 0;
        xQueueReceive(xQueue0, &x0Rx, 10);
        xQueueReceive(xQueue0, &y0Rx, 10);
        xQueueReceive(xQueue0, &z0Rx, 10);

        Serial.println("receive");
        
        //Create messageStr char[]
        itoa(frameNum, frameNumChar, 10);
        strcpy(messageStr, frameNumChar);
        strcat(messageStr, ",");
        itoa(x0Rx, x0Char, 10);    //convert int to char[]
        strcat(messageStr, x0Char);
        strcat(messageStr, ",");
        itoa(y0Rx, y0Char, 10);
        strcat(messageStr, y0Char);
        strcat(messageStr, ",");
        itoa(z0Rx, z0Char, 10);
        strcat(messageStr, z0Char);
        strcat(messageStr, ",");

        len = strlen(messageStr);

        for (int i = 0; i < len; i++) {
          checkSum ^= messageStr[i];
        }
        messageStr[len] = checkSum;
        messageStr[len + 1] = '\n';
        for (int j = 0; j < len + 2; j++) {
          Serial.write(messageStr[j]);
        }

        sendFlag = 1;
        frameNum++;
        readByte = 0;

        xSemaphoreGive(xBinarySemaphore);
        xSemaphoreGive(xMutexSemaphore);
      }
      else if (readByte == 'R'){
        //Resend message
        for (int k = 0; k < len + 2; k++) {
          Serial.write(messageStr[k]);
        }
            readByte = 0;
                xSemaphoreGive(xMutexSemaphore);
      }
      else {
        if (sendFlag)
        {
          counter++;
          if (counter == 30000)
          {
            //Resend message
            for (int m = 0; m < len + 2; m++) {
              Serial.write(messageStr[m]);
            }
            counter = 0;
          }
        }
        xSemaphoreGive(xMutexSemaphore);
      }
    }
  }
  vTaskDelayUntil(&prevWakeTimeSend, 500);
}


void establishContact() {
  int flag = 0;
  while (flag == 0)
  {
    if (Serial.available())
    {
      if (Serial.read() == 'H')
      {
        flag = 1;
      }
    }
  }
  Serial.write('A');   // send a capital A
}

