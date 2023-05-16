//Arduino Magic Cup! - Stefanie Garcia

String command;
int safetyA = 0;
int safetyB = 0;


void setup() {
    pinMode(LED_BUILTIN, OUTPUT);
    pinMode(6, OUTPUT);   // Start/Stop CW/CCW reference
    pinMode(7, OUTPUT);   // Start/Stop (+) Control
    pinMode(8, OUTPUT);   // CW/CCW indicator

    //LEDs for CW vs. CCW indicator
    pinMode(10, OUTPUT);   // CW mode indicator (unfills the cup)
    pinMode(11, OUTPUT);   // CCW mode indicator (refills the cup)
    
    //LEDs for receives John's serial command
    pinMode(12, OUTPUT);  // Recieves Command A
    pinMode(13, OUTPUT);  // Recieves Command B
    
    Serial.begin(9600);
    delay(500); 
    Serial.println("Is the ghost thirsty?");

}
 
void loop() {

int fill_time = 5000;   //NEEDS TO BE CALIBRATED TO EACH SPECIFIC CUP
    
// START Pump in OFF:
//Pump turns off
digitalWrite(6, HIGH); 
digitalWrite(7, HIGH); 
    
    if(Serial.available()){
        command = Serial.readStringUntil('\n');
        Serial.println(command);
        
        if((command.equals("A") && (safetyA == 0))){
           

             //Pump moves into CW (unfills the cup)  
                  digitalWrite(8, LOW); //Switch to CW mode
    
                  //LED indicators turn on
                  digitalWrite(12, HIGH); // Recieves Command A
                  digitalWrite(10, HIGH); // CW mode indicator (unfills the cup)
                  
                  //Pump turns on
                  digitalWrite(6, HIGH);    // Start/Stop CW/CCW reference
                  digitalWrite(7, LOW);     // Start/Stop (+) Control
                  delay(fill_time);         // Pump on CW (unfill the cup) for xx seconds
                 

                  //LED indicators turn off
                  digitalWrite(12, LOW);  // Recieves Command A
                  digitalWrite(10, LOW);  // CW mode indicator (unfills the cup)

                  //Safety check
                   safetyA++;
                   safetyB = 0;
                   Serial.println("Safety B = ");
                   Serial.println(safetyB);
      
                   Serial.println("Safety A = ");
                   Serial.println(safetyA);

                   

        }
        else if((command.equals("B") && (safetyB == 0))){
  
              //Pump moves into CCW (re-fills the cup)  
                  digitalWrite(8, HIGH); //Switch to CCW mode
    
                  //LED indicators turn on
                  digitalWrite(13, HIGH); // Recieves Command B
                  digitalWrite(11, HIGH); // CCW mode indicator (refills the cup)
                  
                  //Pump turns on
                  digitalWrite(6, HIGH);    // Start/Stop CW/CCW reference
                  digitalWrite(7, LOW);     // Start/Stop (+) Control
                  delay(fill_time);         // Pump on CW (unfill the cup) for xx seconds

                  //LED indicators turn off
                  digitalWrite(13, LOW);  // Recieves Command B
                  digitalWrite(11, LOW);  // CCW mode indicator (refills the cup)

                  //Safety check
                    safetyB++;
                    safetyA = 0;
                    Serial.println("Safety B = ");
                    Serial.println(safetyB);

                    Serial.println("Safety A = ");
                    Serial.println(safetyA);

            
        }
            
        else if((command.equals("A") && (safetyA >= 1))) {
          //pump off!
          Serial.println("overflow!");
        }

        else if((command.equals("B") && (safetyB >= 1))) {
          //pump off!
          Serial.println("overflow!");
          
        }
          
        else{
            Serial.println("Try again!");
        }
    }
}
