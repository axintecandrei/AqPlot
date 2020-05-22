
unsigned char tx = 16;         // a String to hold incoming data
unsigned char ready_to_reply = 0;  // whether the string is complete

void setup() {
  // initialize serial:
  Serial.begin(9600);
}

void loop() {
  // print the string when a newline arrives:
  if (ready_to_reply == 1) 
  {
    Serial.write(tx);
  }
}

/*
  SerialEvent occurs whenever a new data comes in the hardware serial RX. This
  routine is run between each time loop() runs, so using delay inside loop can
  delay response. Multiple bytes of data may be available.
*/
void serialEvent() 
{
 unsigned char rx;
  while (Serial.available())
  {
    // get the new byte:
    rx = Serial.read();
    if (rx == 1)
    {
      ready_to_reply ^=1;
    }
  }
}
