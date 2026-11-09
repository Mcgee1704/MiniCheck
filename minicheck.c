#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[])
{
    if (argc == 1) {
        puts("MiniCheck " MINICHECK_VERSION " – Programm erfolgreich gestartet.");
        return 0;
    }
    if (argc == 2 && strcmp(argv[1], "--version") == 0) {
        puts("MiniCheck " MINICHECK_VERSION);
        return 0;
    }
    if (argc == 2 && strcmp(argv[1], "--help") == 0) {
        puts("Aufruf: minicheck [--version | --help]");
        return 0;
    }
    fputs("Unbekanntes Argument. Hilfe mit minicheck --help.\n", stderr);
    return 2;
}
