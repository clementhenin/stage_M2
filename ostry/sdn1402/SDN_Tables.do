*****************************************************************************************************************************************
* Replication of Tables for SDN/14/02 J. D. Ostry, Berg A., Tsangarides C. G., Redistribution, Inequality, and Growth					*
* There are 3 data files to run this do-file. Save the do file and the datasets in one directory.										*
* Input: 																																*		
*		transfers_corr_2014.dta			--	Table 1																						*
*		SDN_5year_average_dataset.dta 	--	Tables 2, 3, 4																				*
*		SDN_spells_dataset.dta 			--	Tables 5 and 6																				*
*																																		*	
* Output: 																																*
*		Tables_SDN.csv																													*
* April 18, 2014																														*
*****************************************************************************************************************************************

clear all
set more off
set memory 3200000

log using "SDN_Tables_log.txt", replace text

******************************************************************************
* Table 1 ********************************************************************
******************************************************************************

use transfers_corr_2014.dta, clear
pwcorr redist_baseline gctaxtotlgdzs gcxpntrftzs sspg_gdp trrh_gdp tsub_gdp soc_exp_gdp tax_gdp, star(0.05)	

******************************************************************************
* Table 2 ********************************************************************
******************************************************************************

use SDN_5year_average_dataset.dta, clear

qui replace redist_baseline=redist_baseline*100

/* Whole sample */
qui areg redist_baseline logincome_pc gini_market i.year, absorb(ifs) cl(ifs)
est store wholesample_1

/* OECD */
areg redist_baseline logincome_pc gini_market i.year if oecd_1975==1, absorb(ifs) cl(ifs)
est store oecd_1

/* NonOECD */
areg redist_baseline logincome_pc gini_market i.year if nonoecd_1975==1, absorb(ifs) cl(ifs)
est store nonoecd_1

/* Producing Table */
esttab wholesample_1 oecd_1 nonoecd_1 using Tables_SDN.csv, ///
		replace drop(*year) order(gini_market logincome_pc ) b(3) se(4) //// 
		label depvars nobrackets star(* 0.10 ** 0.05 *** 0.01) nogaps nonotes addnotes("" "" ) //// 
		stats(N r2, labels("Observations" "R-squared") fmt(0 4)) mtitles("Whole sample" "OECD" "NonOECD") ///
		title("Table 2. Correlation between market inequality and redistribution") 

******************************************************************************
* Table 3 ********************************************************************
******************************************************************************

replace redist_baseline=redist_baseline/100

/* Column 1 */
qui xtabond2 diffyy_5 lny0_5 gini_net redist_baseline i.year, ///
	gmm(lny0_5, lag(1 4) eq(diff)) ///
	gmm(gini_net redist_baseline, lag(1 2) eq(diff)) ///
	gmm(gini_net redist_baseline, lag(1 2) eq(level)) ///
	iv(i.year) twostep h(2) robust
	est store table3_1
	
/* Column 2 */				
qui xtabond2 diffyy_5 lny0_5 gini_net redist_baseline lni lnpopgr i.year, ///
	gmm(lny0_5, lag(1 1) eq(diff)) ///
	gmm(lni lnpopgr gini_net redist_baseline, lag(1 2) eq(diff)) ///
	gmm(lni lnpopgr gini_net redist_baseline, lag(1 1) eq(level)) ///
	iv(i.year) twostep h(2) robust
	est store table3_2
	
/* Column 3 */

qui xtabond2 diffyy_5 lny0_5 gini_net redist_baseline lni lnpopgr ltoted i.year, ///
	gmm(lny0_5, lag(1 1) eq(diff)) ///
	gmm(lni lnpopgr gini_net redist_baseline ltoted, lag(1 1) eq(diff)) ///
	gmm(lni lnpopgr gini_net redist_baseline, lag(1 2) eq(level)) ///
	iv(i.year) twostep h(2) robust 
	est store table3_3
					
/* Column 4 */

qui xtabond2 diffyy_5 lny0_5 gini_net redist_baseline lni lnpopgr db3_l1tttgr ltoted p4polity2 open lmfdebtl i.year, ///
	gmm(lny0_5, lag(1 1) eq(diff)) ///
	gmm(lnpopgr gini_net redist_baseline ltoted, lag(1 1) eq(diff)) ///
	gmm(lnpopgr gini_net redist_baseline, lag(1 2) eq(level)) ///
	iv(i.year ) twostep h(2) robust
	est store table3_4
	
/* Producing Table */
esttab table3_1 table3_2 table3_3 table3_4 using Tables_SDN.csv, ///
		append label drop(*year) dep nogap order(lny0_5 gini_net redist_baseline lni lnpopgr ltoted db3_l1tttgr p4polity2 open lmfdebtl) ///
		stats(N N_g sarganp hansenp ar1p ar2p j, ///
		labels("Observations" "Numbero of ifs" "Sargan" "Hansen" "AR1" "AR2" "InstrumNo") fmt(0 0 4 4 4 4 0 4 4 4 4 4 4 0) ) ///
		b(4) se(4) star(* 0.10 ** 0.05 *** 0.01)  mtitles("Baseline (1)" "Baseline + ctrls (2)" "Baseline + ctrls (3)" "Baseline + ctrls (4)")  ///
		title("Table 3. The effect of inequality and redistributive transfers on growth") nonotes /// 
		addnotes("" "" "")

******************************************************************************
* Table 4 ********************************************************************
******************************************************************************

/* Full sample */
qui xtabond2 diffyy_5 lny0_5 gini_net red_abs_diff i.year, ///
	gmm(lny0_5, lag(1 4) eq(diff)) ///
	gmm(gini_net red_abs_diff, lag(1 2) eq(diff)) ///
	gmm(gini_net red_abs_diff, lag(1 2) eq(level)) ///
	iv(i.year) twostep h(2) robust
	est store table4_1

/* Solt sample */
qui xtabond2 diffyy_5 lny0_5 gini_net red_abs_diff_solt_sample i.year, ///
	gmm(lny0_5, lag(1 4) eq(diff)) /// 
	gmm(gini_net red_abs_diff_solt_sample, lag(1 2) eq(diff)) ///
	gmm(gini_net red_abs_diff_solt_sample, lag(1 2) eq(level)) ///
	iv(i.year) twostep h(2) robust
	est store table4_3

/* Producing Table */
esttab table4_1 table3_1 table4_3 using Tables_SDN.csv, ///
		append label drop(*year) dep nogap order(lny0_5 gini_net redist_baseline ) ///
		stats(N N_g sarganp hansenp ar1p ar2p j, ///
		labels("Observations" "Numbero of ifs" "Sargan" "Hansen" "AR1" "AR2" "InstrumNo") fmt(0 0 4 4 4 4 0 4 4 4 4 4 4 0) ) ///
		b(4) se(4) star(* 0.10 ** 0.05 *** 0.01) mtitles("Full (1)" "Baseline (2)" "Restricted (3)")  ///
		title("Table 4.  Alternative Samples: The Effect of Inequality and Redistributive Transfers on Growth") nonotes /// 
		addnotes("" "" "")

******************************************************************************
* Table 5 ********************************************************************
******************************************************************************

use SDN_spells_dataset.dta, clear

stset year, id(spell_ids_10) fail(acc_stop_10) origin(acc_startpl4_10==1)

/* Column 1 */
qui streg gini_net int_redist_baseline_t25 int_redist_baseline_b75 income_pc_10_0 , d(w) notime 
est store table_5_col1

/* Column 2 */
qui streg gini_net int_redist_baseline_t25 int_redist_baseline_b75 income_pc_10_0 lni lnpopgr, d(w) notime 
est store table_5_col2

/* Column 3 */
qui streg gini_net int_redist_baseline_t25 int_redist_baseline_b75 income_pc_10_0 db3_l1tttgr du3_l1usrategr ltoted , d(w) notime 
est store table_5_col3

/* Column 4 */
qui streg gini_net int_redist_baseline_t25 int_redist_baseline_b75 income_pc_10_0 db3_l1tttgr du3_l1usrategr ltoted p4polity open lmfdebtl , d(w) notime 
est store table_5_col4

/* Producing Table */	
esttab table_5_col1 table_5_col2 table_5_col3 table_5_col4 using Tables_SDN.csv, /// 
	append eform dep b(3) se(4) nogaps order(gini_net int_redist_baseline_t25 int_redist_baseline_b75 income_pc_10_0 lni lnpopgr ltoted db3_l1tttgr du3_l1usrategr p4polity2 open lmfdebtl) /// 
	stats(N N_sub N_fail ll, layout(@  `""@/@""' @ @ @) labels("Observations" "Success/failure" "Log-likelihood") fmt(0 0 0 3)) /// 
	label drop(_cons) nobrackets mtitle("Baseline (1)" "Baseline + ctrls (2)" "Baseline + ctrls (3)" "Baseline + ctrls (4)") title( "Table 5.  The effect of inequality and redistribution on the duration of growth spells") star(* 0.10 ** 0.05 *** 0.01) nonotes addnote("" "" "")
est drop table_5_col1 table_5_col2 table_5_col3 table_5_col4

******************************************************************************
* Table 6 ********************************************************************
******************************************************************************

/* Column 1 */
qui streg gini_net int_redist_baseline_t25 int_redist_baseline_b75 income_pc_10_0 , d(w) notime 
est store table_6_col1

/* Column 2 */
qui streg gini_net int_red_abs_diff_t25 int_red_abs_diff_b75 income_pc_10_0 , d(w) notime 
est store table_6_col2

/* Column 3 */
qui streg gini_net int_red_abs_diff_solt_sample_t25 int_red_abs_diff_solt_sample_b75 income_pc_10_0 , d(w) notime 
est store table_6_col3

/* Producing Table */
esttab table_6_col2 table_6_col1 table_6_col3 using Tables_SDN.csv, append eform dep b(3) se(4) nogaps ///
		order(gini_net int_red_abs_diff_t25 int_red_abs_diff_b75 int_redist_baseline_t25 int_redist_baseline_b75 int_red_abs_diff_solt_sample_t25 int_red_abs_diff_solt_sample_b75 income_pc_10_0) /// 
		stats(N N_sub N_fail ll, layout(@  `""@/@""' @ @ @) labels("Observations" "Success/failure" "Log-likelihood") fmt(0 0 0 3)) /// 
		label drop(_cons) nobrackets title( "Table 6. Alternative samples: transfers inequality and the duration of growth spells") ///
		mtitle("Full" "Baseline" "Restricted") star(* 0.10 ** 0.05 *** 0.01) nonotes addnote("" "" "")
est drop table_6_col1 table_6_col2 table_6_col3 

log close
