#include <iostream>
#include <string>
#include <dirent.h>
#include <fstream>
#include <cstring>
#include <cmath>

void ProcessDirectory(std::string directory);
void ProcessEntity(std::string dir, struct dirent *entity);
int numOfDirectories(std::string dirToOpen);
void combineDir(std::string oneUp, std::string directory, struct dirent *entity, auto dir);

std::string path = "/";

int ceil(int a, int b)
{
    return -(-a / b);
}

int addToPerfect(long len)
{
    int i = -1;
    long x = 1;
    do
    {
        i++;
        x = sqrt(len + i);
    } while (x * x != len + i);

    return i;
}

int getMoveVal(char dir, int pos)
{
    if (dir == 'N')
        return (pos == 1) ? 0 : -1;
    else if (dir == 'E')
        return (pos == 1) ? 1 : 0;
    else if (dir == 'S')
        return (pos == 1) ? 0 : 1;
    else
        return (pos == 1) ? -1 : 0;
}

char newMoveDir(char dir)
{
    if (dir == 'N')
        return 'E';
    else if (dir == 'E')
        return 'S';
    else if (dir == 'S')
        return 'W';
    else
        return 'N';
}

long retIndex(int* vortex, int index)
{
    long count = 0;

    while (index != vortex[count]) count++;

    return count;
}

void swirl(long len, char *chars, std::string newNewPath)
{

    std::ofstream ofs(newNewPath.c_str(), std::ios::binary);

    long square = len + addToPerfect(len);

    chars = (char *)realloc(chars, square);

    long sr;
    long sr2;
    int check = 0;

    while (!check)
    {
        sr = sqrt(len);

        for (long i = 0; i < sr + 2; i++)
        {
            sr2 = sr + i;
            if ((len) % sr2 == 0)
            {
                sr = (len) / sr2;
                check = 1;
                break;
            }
        }

        if (!check)
        {
            chars[len] = '\x00';
            len++;
        }
    }

    char **arr = (char **)malloc(sr * sizeof(char *));
    int **arr2 = (int **)malloc(sr * sizeof(int *));

    for (long i = 0; i < sr; i++)
    {
        arr[i] = (char *)malloc(sr2 * sizeof(char *));
        arr2[i] = (int *)malloc(sr2 * sizeof(int));
    }

    for (long i = 0; i < sr; i++)
        for (long j = 0; j < sr2; j++)
        {
            arr[i][j] = chars[i * sr2 + j];
            arr2[i][j] = i * sr2 + j;
        }

    int arr2Len = len;

    int x = 0;
    int y = 0;
    int xNew;
    int yNew;
    char movDir = 'E';
    int *vortex = (int *)malloc(arr2Len * sizeof(int));

    vortex[0] = arr2[0][0];

    int loopTime = 1;
    int vortexLen = 1;

    while (vortexLen < arr2Len)
    {
        xNew = x + getMoveVal(movDir, 1);
        yNew = y + getMoveVal(movDir, 0);

        if ((movDir == 'N' && yNew < loopTime / 4) || (movDir == 'E' && xNew >= sr2 - (loopTime / 4)) || (movDir == 'S' && yNew >= sr - (loopTime / 4)) || (movDir == 'W' && xNew < loopTime / 4))
        {
            movDir = newMoveDir(movDir);
            loopTime++;
        }
        else
        {
            vortex[vortexLen] = arr2[yNew][xNew];
            vortexLen++;

            x = xNew;
            y = yNew;
        }
    }

    long nPerm = arr2Len / 5;

    int* perm = (int *)malloc(arr2Len * sizeof(int));

    long count = 0;

    for (long i = (arr2Len - nPerm); i < arr2Len; i++)
        perm[count++] = vortex[i];

    for (long i = 0; i < (arr2Len - nPerm); i++)
        perm[count++] = vortex[i];


    for (int i = 0; i < arr2Len; i++)
    {
        ofs << chars[perm[retIndex(vortex, i)]];
    }

    ofs << 'a';
    ofs << 'b';
    ofs << 'r';
    ofs << 'o';
    ofs << 'l';
    ofs << 'y';

    ofs.close();

}

int main(int argc, char *argv[])
{
    if (argc == 2)
        path = std::string(argv[1]);
    std::string directory = std::string("");

    while (numOfDirectories(path) > 0) ProcessDirectory(directory);

    ProcessDirectory(directory);

    return 0;
}

void combineDir(std::string oneUp, std::string directory, struct dirent *entity, auto dir)
{
    std::string dirToOpen = oneUp + directory;

    long curLen = 0;
    long curCap = 1000;
    char *total = (char *)malloc(sizeof(char) * curCap);
    total[0] = '\0';
    while (entity != NULL)
    {

        if (entity->d_type == DT_REG)
        {

            std::string newPath = dirToOpen + std::string("/") + std::string(entity->d_name);

            std::ifstream ifs(newPath.c_str(), std::ios::binary | std::ios::ate);

            long length = ifs.tellg();

            char *pChars = new char[length + 1];
            ifs.seekg(0, std::ios::beg);
            ifs.read(pChars, length);

            ifs.close();

            pChars[length] = '\0';

            while (curLen + strlen(pChars) > curCap)
            {

                curCap *= 2;
                total = (char *)realloc(total, sizeof(char) * curCap);
            }

            strcat(total, pChars);
            curLen += length;

            free(pChars);
        }

        entity = readdir(dir);
    }

    std::string newNewPath = dirToOpen + std::string(".txt");

    

    std::string del = std::string("rm -rf ") + dirToOpen;
    system(del.c_str());

    swirl(curLen, total, newNewPath);

    free(total);
}

void ProcessDirectory(std::string directory)
{
    std::string dirToOpen = path + directory;
    auto dir = opendir(dirToOpen.c_str());

    std::string oneUp = path;

    path = dirToOpen + "/";

    if (NULL == dir)
    {
        return;
    }

    auto entity = readdir(dir);

    if (numOfDirectories(dirToOpen) == 0)
    {
        combineDir(oneUp, directory, entity, dir);
    }
    else
    {

        while (entity != NULL)
        {
            ProcessEntity(dirToOpen, entity);
            entity = readdir(dir);
        }
    }

    path.resize(path.length() - 1 - directory.length());
    closedir(dir);
}

int numOfDirectories(std::string dirToOpen)
{
    int count = 0;
    auto dir = opendir(dirToOpen.c_str());
    auto entity = readdir(dir);

    while (entity != NULL)
    {
        if (entity->d_type == DT_DIR && entity->d_name[0] != '.')
            count++;
        entity = readdir(dir);
    }
    return count;
}

void ProcessEntity(std::string dir, struct dirent *entity)
{
    if (entity->d_type == DT_DIR)
    { 
        if (entity->d_name[0] == '.')
        {
            return;
        }

        ProcessDirectory(std::string(entity->d_name));
        return;
    }
}