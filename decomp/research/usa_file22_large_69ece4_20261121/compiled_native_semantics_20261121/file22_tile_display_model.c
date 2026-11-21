/* Research-only semantic hypothesis for original-USA func_801CC0C4_69ECE4.
 * NOT matching C; NOT incorporated into the game. The input pointer/field
 * offsets and command opcodes are grounded in original ASM, while the host
 * bounds checks are intentionally safer than original division traps.
 * No extracted ROM, original instruction bytes, or game assets are included.
 */
#include <stddef.h>
#include <stdint.h>

/* Big-endian 32-bit guest metadata; 36 bytes, verified at ROM 0x6A7F8C.
 * A host-side adapter must separately map these guest pointers into arrays.
 */
typedef struct File22GuestDesc {
    uint32_t flags_00;       /* +0x00: first halfword used as enable */
    uint32_t page_map_04;    /* +0x04: guest ptr to per-page byte IDs */
    uint32_t tile_ids_08;    /* +0x08: guest ptr to u16 tile IDs */
    uint32_t formats_0C;     /* +0x0C: guest ptr to u16 descriptors */
    uint32_t texture_10;     /* +0x10: texture base guest address */
    uint32_t unknown_14;     /* +0x14: not read in this function */
    uint8_t unknown_18;     /* +0x18 */
    uint8_t unknown_19;     /* +0x19 */
    uint8_t format_1A;      /* +0x1A: 0, 1 or 2 */
    uint8_t unknown_1B;     /* +0x1B */
    int16_t page_cols_1C;   /* +0x1C */
    int16_t page_rows_1E;   /* +0x1E */
    int16_t pixel_width_20; /* +0x20 */
    int16_t pixel_height_22;/* +0x22 */
} File22GuestDesc;

typedef char file22_desc_is_36_bytes[(sizeof(File22GuestDesc)==36)?1:-1];
typedef char file22_mode_offset[(offsetof(File22GuestDesc,format_1A)==26)?1:-1];
typedef char file22_size_offset[(offsetof(File22GuestDesc,pixel_width_20)==32)?1:-1];

typedef struct File22DisplayCommand { uint32_t w0,w1; } File22DisplayCommand;
typedef struct File22ModelInput {
    const uint8_t *pages;
    size_t page_count;
    const uint16_t *tile_ids;
    size_t tile_count;
    const uint16_t *format_entries;
    size_t format_count;
    uint32_t texture_guest_base;
    int16_t page_cols, page_rows, pixel_width, pixel_height;
    uint8_t format;
} File22ModelInput;
typedef struct File22ModelResult {
    size_t tiles_drawn, texture_setup_count, commands_emitted;
    uint16_t last_tile_id;
} File22ModelResult;

static int emit(File22DisplayCommand *out,size_t capacity,size_t *n,uint32_t w0,uint32_t w1) {
    if (*n>=capacity)return 0;
    out[*n].w0=w0;out[*n].w1=w1;++*n;return 1;
}

/* The true game has no display-list capacity or tile array bounds checks.
 * Safe host-only validation must not be mistaken for matching instructions.
 */
int file22_tile_display_model(const File22ModelInput *in,
     File22DisplayCommand *out,size_t capacity,File22ModelResult *report) {
    size_t n=0,tiles_drawn=0,setups=0;
    uint16_t last=0xFFFF;
    int ycell,xcell;
    size_t tiles_per_page;
    if (!in || !out || !report || !in->pages || !in->tile_ids ||
        in->page_cols<=0 || in->page_rows<=0 ||
        in->pixel_width<=0 || in->pixel_height<=0)return 0;
    tiles_per_page=(size_t)(in->pixel_width/32)*(size_t)(in->pixel_height/32);
    if (!tiles_per_page)return 0;
    for (ycell=0;ycell<9;ycell++) {
        int top=ycell*32,bottom=top+31;
        int clipped_top=top<0?0:top,clipped_bottom=bottom>239?239:bottom;
        if (top>=240||bottom<0)continue;
        for (xcell=0;xcell<11;xcell++) {
            int left=xcell*32,right=left+31;
            int clipped_left=left<0?0:left,clipped_right=right>319?319:right;
            size_t page_index,tile_index;
            uint8_t page;
            uint16_t id;
            if (left>=320||right<0)continue;
            page_index=(size_t)((left/in->pixel_width)%in->page_cols)+
                (size_t)in->page_cols*(size_t)((top/in->pixel_height)%in->page_rows);
            if (page_index>=in->page_count)return 0;
            page=in->pages[page_index];
            tile_index=(size_t)page*tiles_per_page+
                (size_t)((left%in->pixel_width)/32)+
                (size_t)(in->pixel_width/32)*(size_t)((top%in->pixel_height)/32);
            if (tile_index>=in->tile_count)return 0;
            id=in->tile_ids[tile_index];
            if (id!=last) {
                uint32_t address,opcode,load;
                last=id;
                if (in->format<=2) {
                    if (in->format==0) {
                        address=in->texture_guest_base+(uint32_t)id*512u;
                        opcode=0xFD100000u;load=0x073FF100u;
                    } else {
                        uint16_t lookup;
                        uint32_t lowshift,highshift;
                        if (!in->format_entries || (size_t)id>=in->format_count)return 0;
                        lookup=in->format_entries[id];
                        lowshift=in->format==1?10u:9u;
                        highshift=in->format==1?6u:5u;
                        address=in->texture_guest_base+
                            (((uint32_t)lookup&0xffu)<<lowshift)+
                            (((uint32_t)lookup&0xf00u)<<highshift);
                        opcode=0xFD500000u;load=in->format==1?0x071FF200u:0x070FF400u;
                    }
                    if (!emit(out,capacity,&n,opcode,address))return 0;
                    if (!emit(out,capacity,&n,in->format==0?0xF5100000u:0xF5500000u,0x07054150u))return 0;
                    if (!emit(out,capacity,&n,0xE6000000u,0))return 0;
                    if (!emit(out,capacity,&n,0xF3000000u,load))return 0;
                    if (!emit(out,capacity,&n,0xE7000000u,0))return 0;
                    if (!emit(out,capacity,&n,in->format==0?0xF5101000u:(in->format==1?0xF5480800u:0xF5400400u),0x00054150u))return 0;
                    if (!emit(out,capacity,&n,0xF2000000u,0x0007C07Cu))return 0;
                    ++setups;
                }
            }
            if (!emit(out,capacity,&n,0xE4000000u|
                    (((uint32_t)(clipped_right*4)&0xfffu)<<12)|
                    ((uint32_t)(clipped_bottom*4)&0xfffu),
                    (((uint32_t)(clipped_left*4)&0xfffu)<<12)|
                    ((uint32_t)(clipped_top*4)&0xfffu)))return 0;
            if (!emit(out,capacity,&n,0xB4000000u,
                    ((uint32_t)((left<0?-left:0)*32)<<16)|
                    ((uint32_t)((top<0?-top:0)*32)&0xffffu)))return 0;
            if (!emit(out,capacity,&n,0xB3000000u,0x10000400u))return 0;
            ++tiles_drawn;
        }
    }
    report->tiles_drawn=tiles_drawn;
    report->texture_setup_count=setups;
    report->commands_emitted=n;
    report->last_tile_id=last;
    return 1;
}
