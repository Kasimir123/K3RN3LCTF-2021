#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define width  11
#define height  2*width + 1

unsigned char state[2*width*width] = { 0 };
int ini = width / 2;

unsigned char strike(unsigned char ray) {

    unsigned char pin;
    unsigned char new_ray;
    signed int res;

    for (int i = 0; i < (2*width+1); i++) {
        pin = state[ini];
        new_ray = pin ^ ray;
        state[ini] = new_ray;
        if (ray <= pin) {
            ini += (width - 1);
        }
        else {
            ini += width;
        }
        if ((i & 1) == 0) {
            res = ini - width - ((i/2) * (2*width - 1));
            if (res == -1) {
                ini += (width - 1);
            }
            if (res == (width - 1)) {
                ini += (1 - width);
            }
        }
        ini %= (2*width*width);
        ray = new_ray;
    }
    
    return ray;
}

const char thunder[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_";

unsigned char *rumble(const unsigned char *in, size_t len)
{
    unsigned char *out;
    size_t  elen;
    size_t  i;
    size_t  j;
    size_t  v;

    elen = 4 * ((len + 2) / 3);
    out  = (unsigned char*)malloc(elen+1);
    out[elen] = '\0';

    for (i=0, j=0; i<len; i+=3, j+=4) {

        v = in[i];
        v = i+1 < len ? v << 8 | in[i+1] : v << 8;
        v = i+2 < len ? v << 8 | in[i+2] : v << 8;

        out[j]   = thunder[(v >> 18) & 0x3F];
        out[j+1] = thunder[(v >> 12) & 0x3F];

        if (i+1 < len) {

            out[j+2] = thunder[(v >> 6) & 0x3F];

        } else {

            out[j+2] = '=';

        }

        if (i+2 < len) {

            out[j+3] = thunder[v & 0x3F];

        } else {

            out[j+3] = '=';

        }
    }

    return out;
}

int main(int argc, char *argv[]) {

    unsigned char *buf;
    unsigned char *rumbuf;
    FILE *victim;
    size_t vfsz;
    long voffend;
    int vrc;

    victim = fopen(argv[1],"rb");
    vrc = fseek(victim, 0, SEEK_END);
    voffend = ftell(victim);
    vfsz = (size_t)voffend;
    buf = (unsigned char*)malloc(vfsz);
    rewind(victim);
    fread(buf, 1, vfsz, victim);
    fclose(victim);

    rumbuf = rumble(buf, vfsz);
    
    for (int j = 0; j < (long)(4 * ((vfsz + 2) / 3)) - 1; j++) {
        rumbuf[j] = strike(rumbuf[j]);  
    }

    FILE *bcrisp;
    bcrisp = fopen("burned.crisp","wb");
    fwrite(rumbuf, 1, (long)(4 * ((vfsz + 2) / 3)), bcrisp);
    fclose(bcrisp);
    free(buf);

    return 0;
}