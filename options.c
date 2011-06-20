/* options -- 2010-05-30
 *
 * 
 */

#include "cummings.h"

USER char *readFile() 
{
  return "hi_level_startup.eec";
}
 int is_options_init;
USER void options_init(int argc, char *argv[])
{
  fprintf(stderr, "options_init()\n"); 
  if( is_options_init++) return; 

}
