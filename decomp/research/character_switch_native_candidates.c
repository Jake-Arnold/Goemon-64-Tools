/* Research-only original-address matching-C candidates for the two retail regions.
 * Compile one SELECT_* and one REGION_* per object with IDO 5.3 -O2 -mips2.
 * Keep outside production manifests until linked-overlay and full-ROM proof.
 */
typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef float f32;

#if defined(REGION_JAPAN)
#define CHARACTER_READER func_801E28B0_59E880
#define CHARACTER_WRAPPER func_801E2888_59E858
#define CHARACTER_SYNC func_801E2970_59E940
#define CURRENT_CHARACTER D_80161DCC_1629CC
#define NEW_CHARACTER_CALLBACK func_801E5B5C_5A1B2C
#define ENGINE_INSTALL func_80034E9C_35A9C
#elif defined(REGION_USA)
#define CHARACTER_READER func_801DD500_599410
#define CHARACTER_WRAPPER func_801DD4D8_5993E8
#define CHARACTER_SYNC func_801DD5C0_5994D0
#define CURRENT_CHARACTER D_8015C5DC_15D1DC
#define NEW_CHARACTER_CALLBACK func_801E0944_59C854
#define ENGINE_INSTALL func_8003522C_35E2C
#else
#error Define REGION_JAPAN or REGION_USA
#endif

#if defined(SELECT_READER)
typedef struct {
    u8 padding[0x5C];
    u8 *state;
} CharacterObject;
u8 CHARACTER_READER(CharacterObject *object) {
    return object->state[0x69];
}
#elif defined(SELECT_WRAPPER)
extern void CHARACTER_SYNC(void *, u8);
void CHARACTER_WRAPPER(void *object, u8 character) {
    CHARACTER_SYNC(object, character);
}
#elif defined(SELECT_SYNC)
extern u32 CURRENT_CHARACTER;
extern void NEW_CHARACTER_CALLBACK(void);
extern void ENGINE_INSTALL(void *, void (*)(void));
#define FIELD8(obj, offset) (*(u8 *)((u8 *)(obj) + (offset)))
#define FIELD16(obj, offset) (*(u16 *)((u8 *)(obj) + (offset)))
#define FIELD32(obj, offset) (*(u32 *)((u8 *)(obj) + (offset)))
#define FIELDF(obj, offset) (*(f32 *)((u8 *)(obj) + (offset)))
#define STATE(obj) ((u8 *)*(void **)((u8 *)(obj) + 0x5C))

/* The unsigned-short ABI is needed to reproduce the original MIPS arg copy. */
void CHARACTER_SYNC(void *object, u16 character) {
    FIELD8(object, 0x60) = character;
    CURRENT_CHARACTER = (u8)character;
    FIELD8(STATE(object), 0x69) = 1;
    FIELD16(STATE(object), 0x86) = 0;
    FIELD16(object, 0x80) = 0;
    FIELD16(STATE(object), 0x30) = 0;
    FIELDF(object, 0xE8) = 0.0f;
    FIELDF(object, 0x68) = 0.0f;
    FIELDF(object, 0x6C) = 0.0f;
    FIELDF(object, 0x70) = 0.0f;
    FIELD16(STATE(object), 0) = 1;
    FIELD32(object, 0x48) = 0;
    FIELD8(object, 0xDB) = 1;
    FIELD8(object, 0x30) &= ~1;
    FIELD8(object, 0xCC) = 0xBA;
    ENGINE_INSTALL(object, NEW_CHARACTER_CALLBACK);
}
#else
#error Define one SELECT_READER, SELECT_WRAPPER or SELECT_SYNC
#endif