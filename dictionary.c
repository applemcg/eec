/*  dictionary --  2006 - 12 - 12
 *    see extern_dictionary.h
 */
#include "cummings.h"
/*           0, LEFT;  1, SAME;  2, RIGHT 
 *
 *  The cummings dictionary is built around the "word".  The collection
 *  of known and used, but unknown words are in the dictionary.  The
 *  parser adds new words to the dictionary.  Any token may be treated,
 *  and probably should be treated as dictionary entry.  There is no
 *  reason why a program of any size couldn't have every token in it's
 *  dictionary.
 *
 * The Public functions expose the individual words, and NOT the ordering
 * methods.
 * A word contains the "word type", a self-referential function call with access
 *    to the remaining attributes, which are
 *  + the word "name", the character string holding the token.
 *  + the word "thred", which for a comment is exactly the same (reference)
 *    as the name, for single storage locations, a value, which may be the 
 *    arrary reference, which itself may be start with a size, followed by
 *    the elements.
 *  + a "count", which reserves space for an integer value, such as a reference
 *    count, a clock tick, ...
 *  + Words may be immediate.  A word is called immediate if it needs to go
 *    into action at "compile" time.  This is an attribute of the word, stored
 *    in the "attrib" value.
 *  + Operations should exist to balance the binary tree.   Any good source
 *    of algorithms, e.g. Knuth, should do the trick.  Taking a page from the
 *    book. the balancing act should happen when the tree grows by a 
 *    certain percent, given a smaller starting size before the first balance
 *    occurs.
 *  + Use the structure and initialization from "Fundamental Algorithms", by 
 *    Binstock & Rex:  top node's right element points a root of tree
 *  + keep "p" and "s" pointers on traverse of tree.
 *  + top structure holds key data:
 *     . comparison function
 *     . duplicates allowed flag
 *     . pointer to tree
 *  + insertion algorithms are type INT, iterative, NOT recursive
 */
/* -------------------------------------------------------------- dntry	--
 */
struct dntry
{
  Word *d_word;		/* runtime properties			*/
  char *name; 		/* all other names use this 		*/
  Dntry *no[3];		/* left, this, right			*/
};
#define N_LEFT 0
#define N_THIS 1
#define N_RIGHT 2

#define d_prt stdout			/* STILL, fix this	*/
/* FILE *d_prt = stderr;		/* fix this !		*/

#define NODE_OF(pw, str)        (1+ecc_strcmp( (str), (pw)->name))
#define PRNODE(pw)		(d_prnode((pw)->d_word))
#define NEXT_NODE(pw, str)	((pw)->no[NODE_OF(pw, str)])
#define DICT_START(pw)		((pw).no[N_RIGHT])

LOCAL void d_usenode( Dntry *p, char *name)
{
	p->name = strsave( name); 
	p->no[N_LEFT] = (Dntry *)NULL; 
	p->no[N_THIS] = p;		/* NEXT_NODE ! */
	p->no[N_RIGHT] = (Dntry *)NULL; 

}
LOCAL int ecc_strcmp( char *p, char *q)
{ 
	int t = strcmp( p, q);
	t = ((t<0)? -1: ((t>0)? 1:0));
	return t; 
}

USER char *strsave(char *s)
{ 
	return (char *)strcpy( malloc( strlen(s) + 1), s); 
}

int d_prctl = 1;
USER void set_prlevel( int n) { d_prctl = n; /* %64 */ }

USER int d_show_search; 

LOCAL void visit_tree( 
		Dntry *node, 
		pfv at_node(Dntry *))
{
	if( node)
	{
		visit_tree( node->no[N_LEFT], at_node);
		at_node( node);
		visit_tree( node->no[N_RIGHT], at_node);
	}
}

LOCAL Dntry top;		/* static, Global Dictionary */
LOCAL int d_count;
LOCAL int d_blank;
 
LOCAL pfv d_stat( Dntry *node)
{
	d_count++;
	if( node->name[0] == (char)NULL) d_blank++;
    return( (pfv)node);
}
LOCAL void d_treestats( Dntry *node) 
{
	d_count = d_blank = 0;
	visit_tree( node, d_stat);
	fprintf(stdout, "DICTIONARY: Count: %d\tBlank: %d\n", d_count, d_blank);
}
LOCAL pfv d_printname( Dntry *node)
{
	fprintf(stdout, "%s\t", node->name);
    return( (pfv)node);
}
LOCAL void d_printnames( Dntry *node)
{
	visit_tree( node, d_printname);
	fprintf(stdout, "\n");
}
LOCAL void d_printtree( Dntry *node) 
{
	if( node)
	{
		d_printtree( node->no[N_LEFT]);
		PRNODE( node);
		d_printtree( node->no[N_RIGHT]);
	}
}

/*
 * ------------------------------------------------------------------ PUBLIC	--
 */
static char errmsg[2048];
USER char *get_dname( char *string)
{
  Dntry *dw = d_search(string);
  sprintf(errmsg, "can't find %s in dictionary", string);
  assertion( 204, (dw != (Dntry *)NULL), errmsg);
  return (d_search(string))->name; 
}
USER Word *getDword(Dntry *dw)
{
  return dw->d_word;
}
USER Dntry *d_search( char *word)
{
	Dntry *onode = &top;
	Dntry *node = DICT_START( top);
	assertion( 201,(onode != (Dntry *)NULL), "d_search:  onode IS null" );
	while( node && onode != node)
	{
		onode = node;
		node = NEXT_NODE(node, word);
	}
	return node;
}
USER void d_stats(char *msg)
{ 
	return; 
	d_treestats( DICT_START( top));
}
USER void d_names() 
{
	d_printnames( DICT_START( top));
}
USER void d_print()  
{
	fprintf( d_prt, "# ------ PRINTING the Whole DICTIONARY\t--\n");
	d_printtree( DICT_START(top));
	fprintf( d_prt, "# ------------------------------------\t--\n");
}
USER Word *get_d_word( Dntry *pD)
{
	return pD->d_word;
}
USER void set_d_word( Dntry *pD, Word *word)
{
	pD->d_word = word;
}
USER Dntry *d_insert( char *name) 
{
	Dntry *onode = &top;
	Dntry *node = DICT_START( top);

	while( node && onode != node)
	{
		onode = node;
		node = NEXT_NODE( node, name);	/* LEFT, SAME, RIGHT, null	*/
	}
	if( !node )
	{
		int t = NODE_OF(onode,name);
		d_usenode( top.no[N_LEFT], name);
		node = onode->no[t] = top.no[N_LEFT];
		onode->no[N_THIS] = onode;	/* node points to self when ? = this */
	        node->d_word = new_word( name);

		top.no[N_LEFT] = New(dntry);	/* to receive next search 	*/
	}
	return node;
}
/*
 * --------------------------------------------------------------- dntry	--
 */
LOCAL int is_dict_init;
USER void dict_init()
{
	if( is_dict_init++) return; 

	/*  new_dntry(); */
	top.no[N_LEFT] = New(dntry);
	top.no[N_THIS] = &top; 
	top.no[N_RIGHT] = New(dntry);

	d_usenode( DICT_START( top), "");

	/* here is where to inject the built-in words ?? */
}

