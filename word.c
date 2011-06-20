/* word -- 2010-05-22
 *
 * 
 */

#include "cummings.h"

/* --------------------------------------------------------------- Word	--
 */
struct word
{
	long w_value;		/* constant, variable 			*/
	char *w_name; 		/* "the text of the word"		*/
	long w_code; 		/*  the instruction CODE 		*/
};

static Type *biZero;
static Type *biLast;

int d_prctl;
#define d_prt stdout
# define PR_ELEM(n,  s, fmt, t)		\
  if(n & d_prctl) { 			\
    fprintf(d_prt,"%s:\t", s);			\
    fprintf(d_prt, fmt, t);		} 

USER Word *new_word ( char *name)
{
  Word *p = New( word);
  p->w_name = get_dname( name);
  return p; 
}
USER Dntry *thisWord( char *name, long val, long code)
{
  Dntry *dw =  d_insert( name);
  Word *w =    getDword( dw);
  w->w_value = val;
  w->w_code = code;
  return dw; 
}
USER void idBiType(Type *biOrigin, Type *biEnd)
{
  biZero = biOrigin;
  biLast = biEnd;
}
USER Type *isTyped(Dntry *dw)
{
  Word *pw = getDword(dw);
  Type *pt = (Type *)pw->w_value;
  return (((biZero<=pt) && (pt<=biLast))? pt: (Type *)NULL);
}
LOCAL void set_builtin( Word *wd, int code, pfv built_in)
{
  /*	  wd->w_funct = built_in; */
	  wd->w_value = (long)code;
}
USER pfv get_thred( Word *tocall)
{
  	/* return tocall->peec->funct; */
  /*  	return tocall->w_funct; */
    return (pfv)0;
}
USER void d_prnode( Word *p)
{
	PR_ELEM(  1, "Name", "%s\n", p->w_name)
	  /*	PR_ELEM(  2, "Funct", "%x\n",p-> w_funct) */
	PR_ELEM(  8, "Value", "%d\n", p->w_value)
}

	Word *wd;       /* UNUSED */
USER void name_function( char *name, pfv funct)
{
	Dntry *pd	= d_insert( name);
	wd	= get_d_word(pd);
	/*	wd->w_funct	= funct; */
}

LOCAL int is_word_init;
USER void word_init()
{
  fprintf(stderr, "word_init()\n"); 
  if( is_word_init++) return; 

}
