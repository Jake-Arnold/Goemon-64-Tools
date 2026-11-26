/* TEST FIXTURE ONLY. Minimal ABI model for synthetic tests; not the SDK. */
#ifndef GOEMON_TEST_M64P_PLUGIN_H
#define GOEMON_TEST_M64P_PLUGIN_H
#define EXPORT __attribute__((visibility("default")))
#define CALL
#define PLUGIN_NONE 1
#define CONT_TYPE_STANDARD 0
typedef void *m64p_dynlib_handle;
typedef enum {M64ERR_SUCCESS=0,M64ERR_NOT_INIT=1,M64ERR_ALREADY_INIT=2} m64p_error;
typedef enum {M64PLUGIN_INPUT=4} m64p_plugin_type;
typedef struct {int Present, RawData, Plugin, Type;} CONTROL;
typedef struct {CONTROL *Controls;} CONTROL_INFO;
typedef union {
    unsigned Value;
    struct { unsigned R_DPAD:1,L_DPAD:1,D_DPAD:1,U_DPAD:1,START_BUTTON:1,Z_TRIG:1,B_BUTTON:1,A_BUTTON:1;
        unsigned R_CBUTTON:1,L_CBUTTON:1,D_CBUTTON:1,U_CBUTTON:1,R_TRIG:1,L_TRIG:1,Reserved1:1,Reserved2:1;
        signed X_AXIS:8,Y_AXIS:8; };
} BUTTONS;
#endif
