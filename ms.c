#include <stdio.h>
#include <stdlib.h>
#include <time.h>
void merge(int arr[], int left, int mid, int right)
{
    int n1 = mid - left + 1;
    int n2 = right - mid;
    int *L = malloc(n1 * sizeof(int));
    int *R = malloc(n2 * sizeof(int));
    for (int i = 0; i < n1; i++)
        L[i] = arr[left + i];

    for (int i = 0; i < n2; i++)
        R[i] = arr[mid + 1 + i];

    int i = 0, j = 0, k = left;

    while (i < n1 && j < n2)
    {
        if (L[i] <= R[j])
            arr[k++] = L[i++];
        else
            arr[k++] = R[j++];
    }
    while (i < n1)
    arr[k++] = L[i++];
    while (j < n2)
    arr[k++] = R[j++];
    free(L);
    free(R);
}

void mergeSort(int arr[], int left, int right)
{
    if (left >= right)
    return;
    int mid = (left+right)/ 2;
    mergeSort(arr, left, mid);
    mergeSort(arr, mid + 1, right);
    merge(arr, left, mid, right);
}

int main()
{
    int *arr = malloc(1000000*sizeof(int));
    if (arr == NULL)
    return 0;
    int sizes[] = {1000, 10000, 100000, 1000000};
    int count = 4;
    for (int i = 0; i < count; i++)
    {
        int n = sizes[i];
        for (int j = 0; j < n; j++)
        arr[j] = n - j;
        clock_t start = clock();
        mergeSort(arr, 0, n - 1);
        clock_t end = clock();
        double time_taken =(double)(end - start) / CLOCKS_PER_SEC;
        printf("%d %f\n", n, time_taken);
    }
    free(arr);
    return 0;
}