#define X_STEP_PIN         54
#define X_DIR_PIN          55
#define X_ENABLE_PIN       38
#define X_MIN_PIN           3
#define X_MAX_PIN           2

#define Y_STEP_PIN         60
#define Y_DIR_PIN          61
#define Y_ENABLE_PIN       56
#define Y_MIN_PIN          14
#define Y_MAX_PIN          15

#define Z_STEP_PIN         46
#define Z_DIR_PIN          48
#define Z_ENABLE_PIN       62
#define Z_MIN_PIN          18
#define Z_MAX_PIN          19

//#define LED_PIN            13

//#define PS_ON_PIN          12
//#define KILL_PIN           -1

double X_STEP_SIZE = 100; // step size for 1mm travel distance

void setup() {
  Serial.begin(9600);  
  pinMode(X_STEP_PIN,OUTPUT);
  pinMode(X_DIR_PIN,OUTPUT);
  pinMode(X_ENABLE_PIN,OUTPUT);
  
  pinMode(Y_STEP_PIN,OUTPUT);
  pinMode(Y_DIR_PIN,OUTPUT);
  pinMode(Y_ENABLE_PIN,OUTPUT);
  
  pinMode(Z_STEP_PIN,OUTPUT);
  pinMode(Z_DIR_PIN,OUTPUT);
  pinMode(Z_ENABLE_PIN,OUTPUT);
  
  digitalWrite(X_ENABLE_PIN,LOW);
  digitalWrite(Y_ENABLE_PIN,LOW);
  digitalWrite(Z_ENABLE_PIN,LOW);

  pinMode(X_MIN_PIN,INPUT_PULLUP);
  //digitalWrite(X_MIN_PIN, HIGH);
}

void loop () {
//  home_X();

  int x_minEndstop_state = digitalRead(X_MIN_PIN);
  if (x_minEndstop_state==HIGH){
    Serial.println("pressed");
    Serial.flush();
    delay(5);
  }
  if(x_minEndstop_state==LOW){
    Serial.println("released");
    Serial.flush();
    delay(5);
  }

//  Serial.println("1");
//  delay(500);
//  Serial.println("2");
//  delay(500);

//  move_X(HIGH,1);
//  delay(500);
//  move_X(LOW,1);
//  delay(500);
}

String move_X(bool dir, double dis){
  digitalWrite(X_DIR_PIN,dir);
  for(int i=1;i<=round(X_STEP_SIZE*dis);i++){
  digitalWrite(X_STEP_PIN    , HIGH);
  digitalWrite(X_STEP_PIN    , LOW);
  delay(1);
  }
}

String home_X(){
  bool x_minEndstop_state = digitalRead(X_MIN_PIN);
  while(x_minEndstop_state==LOW){
    move_X(HIGH,1);
  }
}
