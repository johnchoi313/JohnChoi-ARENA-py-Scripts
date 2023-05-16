void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(6, OUTPUT);   // Start/Stop CW/CCW reference
  pinMode(7, OUTPUT);   // Start/Stop (+) Control
  pinMode(8, OUTPUT);   // CW/CCW indicator

  //LEDs for CW vs. CCW indicator
  pinMode(10, OUTPUT);   // CW mode (unfills the cup)
  pinMode(11, OUTPUT);   // CCW mode (refills the cup)
  
  //LEDs for receives John's serial command
  pinMode(12, OUTPUT);  // Recieves Command A
  pinMode(13, OUTPUT);  // Recieves Command B

}

void loop() {

  //Pump moves CW (unfills the cup)
  // Switch to CW mode
    digitalWrite(8, LOW);
    
      //Pump turns off
      digitalWrite(6, HIGH); 
      digitalWrite(7, HIGH); 
      delay(2000);        // Pump off for xx seconds
      digitalWrite(10, HIGH); 
      //Pump turns on
      digitalWrite(6, HIGH);
      digitalWrite(7, LOW); 
      delay(10000);         // Pump on CW (unfill the cup) for xx seconds
      digitalWrite(10, LOW); 


   //Pump moves CCW (fills the cup)
   // Switch to CCW mode
    digitalWrite(8, HIGH);
    
      //Pump turns on
      digitalWrite(6, HIGH); 
      digitalWrite(7, HIGH); 
      delay(2000);        // Pump off for xx seconds
      digitalWrite(11, HIGH); 
  
      //Pump turns off
      digitalWrite(6, HIGH);
      digitalWrite(7, LOW); 
      delay(10000);         // Pump on CCW (refill the cup) for xx seconds
      digitalWrite(11, LOW); 

}
