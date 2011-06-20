/*
 * -------------------------------------- cummings MAIN	--
 *
 *   function ( arg, arg( x,y), ... )
 *     where "\" escapes any single character, 
 *    and an "arg" may have white-space, non-leading, trailing. 
 *    
 * ----------------------------------------------------	-- 
 *    The first application is a browser:
 *         - memory, dictionary, ...
 * ----------------------------------------------------	-- 
 *
 */
#include <stdio.h>

int main( int argc, char *argv[]) 
{ 
/* the various "init"s should
  * a. defend themselves against multiple visits, and
  * b. invoke their own dependent initializations
   */
  options_init( argc, argv);
  compiler_init();
  dict_init();
  runtime_init();
  parserobj_init();

  parser();
  return 0;
}
