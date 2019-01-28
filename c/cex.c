//
// C func example
//


#include <stdio.h>

int main( ) {

       char msg[100];
       
       while (1) {

           //read
           gets( msg );

           //log
           fprintf(stderr, "read msg %s\n", msg);

           //send
           puts( msg );


       };
       
       return 0;
}
