typedef unsigned short u16;
extern void *func_800136A4_142A4(u16);
void *func_80013654_14254(u16 *entry) {
    u16 id = *entry;
    void *result;
    if (id != 0) {
        do {
            result = func_800136A4_142A4(id);
            entry++;
            id = *entry;
        } while (id != 0);
    }
    return result;
}
