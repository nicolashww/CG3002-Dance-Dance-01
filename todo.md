# To-do by 29 Oct

## Hardware
  1. Velcro accelerometers to 4 parts, assuming person is standing upright hands by side as reference **To be done before meeting on Sunday**
      - Purpose is consistency, i.e. the x0 value will be the same direction if velcro taken off and worn again
      1. `Right upper arm`, right above elbow, accelerometer facing outwards (right)
      2. `Left wrist`, right under where pulse is taken, accelerometer facing outwards (left)
      3. `Right upper thigh`, right above knee, accelerometer facing outwards (right)
      4. `Left ankle`, right above shoe, accelerometer facing  outwards (right)
  2. Systems (Raspberry Pi, Arduino, Powerbanks) attached onto belt **To be done on Sunday itself, design how to attach and source/prepare materials beforehand**

## Firmware
  1. Fix the frequency of data sent/received to 50Hz (remember what to change to change frequency in case Pi can't keep up and need to lower) **To be done before meeting on Sunday**
  2. Get handshake working to ensure data is correct **To be done before meeting on Sunday**
  3. Debug corrupt data if any **To be done before meeting on Sunday**

## Software
  1. Ignore first few readings **To be done before meeting on Sunday**
  2. Prepare one slow and one fast pre-processing technique **To be done before meeting on Sunday**
      1. To test if Pi can meet 50Hz (or faster or slower)
  3. Prepare method to learn from raw data **To be done before meeting on Sunday**
