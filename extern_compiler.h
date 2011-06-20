extern void assertion(int ex, int cond, char *errmsg);
extern void pushData( long d) ;
extern long *pData();
extern long popData ();
extern void eec_error( char *fmt, char *tok, int num);
extern void eec_parser( );
extern void compiler_init();
