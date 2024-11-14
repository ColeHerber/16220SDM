#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/timer.h"
#include "hardware/uart.h"
#include "hardware/pwm.h"


int64_t alarm_callback(alarm_id_t id, void *user_data) {
    // Put your timeout handler code in here
    return 0;
}

typedef struct motor_pins {
    uint8_t pwm_pin;
    uint8_t A_pin;
    uint8_t B_pin;
} motor;

// UART defines
// By default the stdout UART is `uart0`, so we will use the second one
#define UART_ID uart0
#define BAUD_RATE 9600

// Use pins 8 and 9 for UART1
// Pins can be changed, see the GPIO function select table in the datasheet for information on GPIO assignments
#define UART_TX_PIN 0
#define UART_RX_PIN 1


//PWM CONSTANTS
#define wrap 255 //MAX INT VAL POSSIBLE
#define scaleFactor 0xFFFF
#define motorCount 2
motor motors[motorCount] = {
    { .pwm_pin = 2, .A_pin = 4, .B_pin = 5 },
    { .pwm_pin = 3, .A_pin = 6, .B_pin = 7 }
};


void message_handler(){
    size_t len = 3;
    uint8_t message[len];
    uart_read_blocking(UART_ID, message, len);

    
    int speed = message[0];
    int dir = message[1]; //0 or 1(modding for saftey)
    int motor = message[2]; //0 or 1(saftey %motorCount to not reach anything else, not bool because maybe more motors in future)

    pwm_set_gpio_level(PICO_DEFAULT_LED_PIN,(speed*scaleFactor)/wrap); // Motor0 0 speed

    pwm_set_gpio_level(motors[motor].pwm_pin,(speed*scaleFactor)/wrap);
    if (speed == 0){
        //DIRECTION SPECIFIES BRAKE OR COAST WHEN SPEED IS 0
        gpio_put(motors[motor].A_pin, dir);  
        gpio_put(motors[motor].B_pin, dir);  
    }
    else{
        if (dir == 0){ //0 for forwards
            gpio_put(motors[motor].A_pin, 1);  
            gpio_put(motors[motor].B_pin, 0);  
        } else{
            gpio_put(motors[motor].A_pin, 0);  
            gpio_put(motors[motor].B_pin, 1);  
        }
    }
    

}

void setup_pwm(uint pin) {
    gpio_set_function(pin, GPIO_FUNC_PWM);

    uint slice_num = pwm_gpio_to_slice_num(pin);

    pwm_set_wrap(slice_num, wrap);  

    pwm_config config = pwm_get_default_config();
    // Set divider, reduces counter clock to sysclock/this value
    pwm_config_set_clkdiv(&config, 4.f);
    // Load the configuration into our PWM slice, and set it running.
    pwm_init(slice_num, &config, true);
}

void setup_toggle(uint pin){
    gpio_init(pin);
    gpio_set_dir(pin, GPIO_OUT);
}

void setup_uart(void){
        
    // For more examples of timer use see https://github.com/raspberrypi/pico-examples/tree/master/timer

    // Set up our UART
    uart_init(UART_ID, BAUD_RATE);


    // Set the TX and RX pins by using the function select on the GPIO
    // Set datasheet for more information on function select
    gpio_set_function(UART_TX_PIN, GPIO_FUNC_UART);
    gpio_set_function(UART_RX_PIN, GPIO_FUNC_UART);

    // Set UART flow control CTS/RTS, we don't want these, so turn them off
    uart_set_hw_flow(UART_ID, false, false);

    // // Set our data format
    // uart_set_format(UART_ID, DATA_BITS, STOP_BITS, PARITY);

    // Turn off FIFO's - we want to do this character by character
    uart_set_fifo_enabled(UART_ID, false);

    
    // Use some the various UART functions to send out data
    // In a default system, printf will also output via the default UART
    int UART_IRQ = UART_ID == uart0 ? UART0_IRQ : UART1_IRQ;

    // And set up and enable the interrupt handlers
    irq_set_exclusive_handler(UART_IRQ, message_handler);
    irq_set_enabled(UART_IRQ, true);

    // Now enable the UART to send interrupts - RX only
    uart_set_irq_enables(UART_ID, true, false);

    // Send out a string, with CR/LF conversions
    uart_puts(UART_ID, " Hello, UART!\n");
}

int main()
{
    
    stdio_init_all();

    //SETUP PINS
    
    setup_pwm(motors[0].pwm_pin);
    setup_pwm(motors[1].pwm_pin);
    setup_pwm(PICO_DEFAULT_LED_PIN);

    setup_toggle(motors[0].A_pin);
    setup_toggle(motors[0].B_pin);
    setup_toggle(motors[1].A_pin);
    setup_toggle(motors[1].B_pin);
    
    //setup serial
    setup_uart();

    sleep_ms(50);

    // pwm_set_gpio_level(motors[0].pwm_pin,(255*scaleFactor)/wrap); // Motor0 0 speed
    // pwm_set_gpio_level(motors[1].pwm_pin,(128*scaleFactor)/wrap); // Motor1 0 speed

     //INITIALIZE TO BRAKE MODE BY DEFAULT
    pwm_set_gpio_level(motors[0].pwm_pin,0);
    pwm_set_gpio_level(motors[1].pwm_pin,0);
    

    gpio_put(motors[0].A_pin, 1);  // Motor0 GPIO_A pin HIGH
    gpio_put(motors[0].B_pin, 1);  // Motor0 GPIO_B pin HIGH

    gpio_put(motors[1].A_pin, 0);  // Motor1 GPIO_A pin HIGH
    gpio_put(motors[1].B_pin, 0);  // Motor1 GPIO_B pin HIGH


    while (1){
        tight_loop_contents();     
    }
       
    

}
