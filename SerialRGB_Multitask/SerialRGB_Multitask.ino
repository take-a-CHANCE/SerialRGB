enum pattern {NONE, FADE, JUMP, BLINK};

class LedStrip
{
	int red;
	int green;
	int blue;
	
public:
	pattern ActivePattern;

	unsigned long Interval;
	unsigned long lastUpdate;

	uint32_t Color1, Color2; // What colors are in use
	uint16_t TotalSteps; // total number of steps in the pattern
	uint16_t Index; // current step within the pattern
	
	void(*OnComplete)(); // Callback on completion of pattern
	
	LedStrip(int redPin, int greenPin, int bluePin, void(*callback)())
	{
		red = redPin;
		pinMode(red, OUTPUT);
		green = greenPin;
		pinMode(green, OUTPUT);
		blue = bluePin;
		pinMode(blue, OUTPUT);

		OnComplete = callback;
	}

	void Update() {
		if ((millis() - lastUpdate) > Interval) // time to update
		{
			lastUpdate = millis();
			switch (ActivePattern)
			{
			case FADE:
				FadeUpdate();
				break;
			case JUMP:
				JumpUpdate();
				break;
			case BLINK:
				BlinkUpdate();
				break;
			default:
				break;
			}
		}
	}

	void Increment() {
		Index++;
		if (Index >= TotalSteps)
		{
			Index = 0;
			if (OnComplete != NULL)
			{
				OnComplete(); // call the comlpetion callback
			}
		}
	}

	// Color making and getting
	uint32_t Color(uint8_t r, uint8_t g, uint8_t b) {
		return ((uint32_t)r << 16) | ((uint32_t)g << 8) | b;
	}
	// Returns the Red component of a 32-bit color
	uint8_t Red(uint32_t color) {
		return (color >> 16) & 0xFF;
	}
	// Returns the Green component of a 32-bit color
	uint8_t Green(uint32_t color) {
		return (color >> 8) & 0xFF;
	}
	// Returns the Blue component of a 32-bit color
	uint8_t Blue(uint32_t color) {
		return color & 0xFF;
	}

	// Sets the strip's color
	void ColorSet(uint32_t color) {
		analogWrite(red, Red(color));
		analogWrite(green, Green(color));
		analogWrite(blue, Blue(color));
	}

	void Fade(uint32_t color1, uint32_t color2, uint16_t steps, uint8_t interval)
	{
		ActivePattern = FADE;
		Interval = interval;
		TotalSteps = steps;
		Color1 = color1;
		Color2 = color2;
		Index = 0;
	}
	void FadeUpdate()
	{
		uint8_t red = ((Red(Color1) * (TotalSteps - Index)) + (Red(Color2) * Index)) / TotalSteps;
		uint8_t green = ((Green(Color1) * (TotalSteps - Index)) + (Green(Color2) * Index)) / TotalSteps;
		uint8_t blue = ((Blue(Color1) * (TotalSteps - Index)) + (Blue(Color2) * Index)) / TotalSteps;
		ColorSet(Color(red, green, blue));
		Increment();
	}

	void Jump(uint16_t interval) {
		ActivePattern = JUMP;
		Interval = interval;
		TotalSteps = 3;
		Index = 0;
	}
	void JumpUpdate() {
		if (Index == 1) { //red
			ColorSet(Color(255, 0, 0));
		}
		else if (Index == 2) { //green
			ColorSet(Color(0, 255, 0));
		}
		else { // blue
			ColorSet(Color(0, 0, 255));
		}
		Increment();
	}

	void Blink(uint32_t color, uint16_t interval) {
		ActivePattern = BLINK;
		Color1 = color;
		Interval = interval;
		TotalSteps = 2;
		Index = 0;
	}
	void BlinkUpdate() {
		if (Index == 1) {
			ColorSet(Color1);
		}
		else {
			ColorSet(Color(0, 0, 0));
		}
		Increment();
	}
};

LedStrip Strip1(3, 5, 6, &Strip1Complete);
LedStrip Strip2(9, 10, 11, &Strip2Complete);

uint32_t RedVal = Strip1.Color(255, 0, 0);
uint32_t YellowVal = Strip1.Color(255, 255, 0);
uint32_t GreenVal = Strip1.Color(0, 255, 0);
uint32_t TealVal = Strip1.Color(0, 255, 255);
uint32_t BlueVal = Strip1.Color(0, 0, 255);
uint32_t VioletVal = Strip1.Color(255, 0, 255);

void setup()
{
	Serial.begin(115200);
	//Startup strips as color for easy power on
	Strip1.ColorSet(Strip1.Color(255, 0, 0)); //Startup as red
	Strip2.ColorSet(Strip2.Color(255, 255, 255)); //Startup as white
}

int slow;
int bright;
int red;
int green;
int blue;
uint32_t color;

void loop()
{

	if (Serial.available() >= 2) {
		int strand = Serial.parseInt();
		switch (Serial.read())
		{
		case 'f':
			slow = Serial.parseInt();
			bright = Serial.parseInt();
			if (Serial.read() == '\n') {
				if (strand == 1) {
					Strip1.Color1 = VioletVal;
					Strip1.Color2 = RedVal;
					Strip1.Fade(Strip1.Color1, Strip1.Color2, 255, slow);
				}
				else if (strand == 2) {
					Strip2.Fade(VioletVal, RedVal, 255, slow);
				}
				else if (strand == 3) {
					Strip1.Fade(VioletVal, RedVal, 255, slow);
					Strip2.Fade(VioletVal, RedVal, 255, slow);
				}
			}
			break;
		case 'c':
			if (strand == 1) {
				Strip1.ActivePattern = NONE;
				Strip1.ColorSet(Strip1.Color(0, 0, 0));
			}
			else if (strand == 2) {
				Strip2.ActivePattern = NONE;
				Strip2.ColorSet(Strip2.Color(0, 0, 0));
			}
			else if (strand == 3) {
				Strip1.ActivePattern = NONE;
				Strip1.ColorSet(Strip1.Color(0, 0, 0));
				Strip2.ActivePattern = NONE;
				Strip2.ColorSet(Strip2.Color(0, 0, 0));
			}
			break;
		case 'j':
			slow = Serial.parseInt();
			if (Serial.read() == '\n') {
				if (strand == 1) {
					Strip1.Jump(slow);
				}
				else if (strand == 2) {
					Strip2.Jump(slow);
				}
				else if (strand == 3) {
					Strip1.Jump(slow);
					Strip2.Jump(slow);
				}
			}
			break;
		case 'b':
			slow = Serial.parseInt();
			red = Serial.parseInt();
			green = Serial.parseInt();
			blue = Serial.parseInt();
			color = Strip1.Color(red, green, blue);
			if (Serial.read() == '\n'){
				if (strand == 1) {
					Strip1.Blink(color, slow);
				}
				else if (strand == 2) {
					Strip2.Blink(color, slow);
				}
				else if (strand == 3) {
					Strip1.Blink(color, slow);
					Strip2.Blink(color, slow);
				}
			}
			break;
		case ',':
			red = Serial.parseInt();
			green = Serial.parseInt();
			blue = Serial.parseInt();
			color = Strip1.Color(red, green, blue);
			if (Serial.read() == '\n') {
				if (strand == 1) {
					Strip1.ActivePattern = NONE;
					Strip1.ColorSet(color);
				}
				else if (strand == 2) {
					Strip2.ActivePattern = NONE;
					Strip2.ColorSet(color);
				}
				else if (strand == 3) {
					Strip1.ActivePattern = NONE;
					Strip1.ColorSet(color);
					Strip2.ActivePattern = NONE;
					Strip2.ColorSet(color);
				}
			}
			break;
		default:
			break;
		}
	}
	Strip1.Update();
	Strip2.Update();

}

//------------------------------------------------------------
//Completion Routines - get called on completion of a pattern (pretty much just fade)
//------------------------------------------------------------

void Strip1Complete() {
	if (Strip1.ActivePattern == FADE) {
		Strip1.Color1 = Strip1.Color2;
		if (Strip1.Color1 == RedVal) {
			Strip1.Color2 = YellowVal;
		}
		else if (Strip1.Color1 == YellowVal) {
			Strip1.Color2 = GreenVal;
		}
		else if (Strip1.Color1 == GreenVal) {
			Strip1.Color2 = TealVal;
		}
		else if (Strip1.Color1 == TealVal) {
			Strip1.Color2 = BlueVal;
		}
		else if (Strip1.Color1 == BlueVal) {
			Strip1.Color2 = VioletVal;
		}
		else if (Strip1.Color1 == VioletVal) {
			Strip1.Color2 = RedVal;
		}
		else {
			Strip1.Color2 = Strip1.Color(255, 255, 255);
		}
	}
}

void Strip2Complete() {
	if (Strip2.ActivePattern == FADE) {
		Strip2.Color1 = Strip2.Color2;
		if (Strip2.Color1 == RedVal) {
			Strip2.Color2 = YellowVal;
		}
		else if (Strip2.Color1 == YellowVal) {
			Strip2.Color2 = GreenVal;
		}
		else if (Strip2.Color1 == GreenVal) {
			Strip2.Color2 = TealVal;
		}
		else if (Strip2.Color1 == TealVal) {
			Strip2.Color2 = BlueVal;
		}
		else if (Strip2.Color1 == BlueVal) {
			Strip2.Color2 = VioletVal;
		}
		else if (Strip2.Color1 == VioletVal) {
			Strip2.Color2 = RedVal;
		}
		else {
			Strip2.Color2 = Strip2.Color(255, 255, 255);
		}
	}
}