import os

#os.system("python -m pm4py.cli DiscoverPetriNetAlpha tests\\input_data prova2")
#os.system("python -m pm4py.cli DiscoverPetriNetInductive tests\\input_data prova2")
#os.system("python -m pm4py.cli DiscoverPetriNetHeuristics tests\\input_data prova2")
#os.system("python -m pm4py.cli DiscoverBPMNInductive tests\\input_data prova2")
#os.system("python -m pm4py.cli DiscoverProcessTreeInductive tests\\input_data prova2")
#os.system("python -m pm4py.cli ConformanceDiagnosticsTBR tests\\input_data\\running-example.xes tests\\input_data\\running-example.pnml result_diagnostics_tbr.txt")
#os.system("python -m pm4py.cli ConformanceDiagnosticsAlignments tests\\input_data\\running-example.xes tests\\input_data\\running-example.pnml result_diagnostics_alignments.txt")
#os.system("python -m pm4py.cli FitnessTBR tests\\input_data\\running-example.xes tests\\input_data\\running-example.pnml result_fitness_tbr.txt")
#os.system("python -m pm4py.cli FitnessAlignments tests\\input_data\\running-example.xes tests\\input_data\\running-example.pnml result_fitness_alignments.txt")
#os.system("python -m pm4py.cli PrecisionTBR tests\\input_data\\running-example.xes tests\\input_data\\running-example.pnml result_precision_tbr.txt")
#os.system("python -m pm4py.cli PrecisionAlignments tests\\input_data\\running-example.xes tests\\input_data\\running-example.pnml result_precision_alignments.txt")
#os.system("python -m pm4py.cli ConvertToXES tests\\input_data\\running-example.csv result_ru.xes")
#os.system("python -m pm4py.cli ConvertToCSV tests\\input_data\\running-example.xes result_ru.csv")
#os.system("python -m pm4py.cli ConvertPNMLtoBPMN tests\\input_data\\running-example.pnml result_bpmn1.bpmn")
#os.system("python -m pm4py.cli ConvertPNMLtoPTML tests\\input_data\\running-example.pnml result_ptml1.ptml")
#os.system("python -m pm4py.cli ConvertPTMLtoPNML tests\\input_data\\running-example.ptml result_pnml1.pnml")
#os.system("python -m pm4py.cli ConvertPTMLtoBPMN tests\\input_data\\running-example.ptml result_bpmn2.bpmn")
#os.system("python -m pm4py.cli ConvertBPMNtoPNML tests\\input_data\\running-example.bpmn result_pnml3.pnml")
#os.system("python -m pm4py.cli ConvertDFGtoPNML tests\\input_data\\running-example.dfg result_pnml4.pnml")
#os.system("python -m pm4py.cli DiscoverDFG tests\\input_data\\running-example.xes result_dfgdisc.dfg")
#os.system("python -m pm4py.cli ConvertDFGtoPNML result_dfgdisc.dfg result_dfgdisc_conv.pnml")
#os.system("python -m pm4py.cli SaveVisDFG result_dfgdisc.dfg visual_dfg.png")
#os.system("python -m pm4py.cli SaveVisPNML result_pnml1.pnml visual_petri.png")
#os.system("python -m pm4py.cli SaveVisBPMN result_bpmn1.bpmn visual_bpmn.png")
#os.system("python -m pm4py.cli SaveVisPTML result_ptml1.ptml visual_process_tree.png")
#os.system("python -m pm4py.cli SaveVisDottedChart tests\\input_data\\running-example.xes time:timestamp case:concept:name concept:name vis_dotted.png")
#os.system("python -m pm4py.cli SaveVisTransitionSystem tests\\input_data\\running-example.xes vis_trans_system.png")
#os.system("python -m pm4py.cli SaveVisTrie tests\\input_data\\running-example.xes vis_trie.png")
#os.system("python -m pm4py.cli SaveVisEventsDistribution tests\\input_data\\running-example.xes days_week vis_ev_distr.png")
#os.system("python -m pm4py.cli SaveVisEventsPerTime tests\\input_data\\running-example.xes vis_ev_time.png")
#os.system("python -m pm4py.cli GenerateProcessTree 10 result_ptandloggenerator.ptml")
#os.system("python -m pm4py.cli PNMLplayout tests\\input_data\\running-example.pnml result_playout1.xes")
#os.system("python -m pm4py.cli PTMLplayout tests\\input_data\\running-example.ptml result_playout2.xes")
#os.system("python -m pm4py.cli DFGplayout tests\\input_data\\running-example.dfg result_playout3.xes")
os.system("python -m pm4py.cli SaveVisSNA tests\\input_data\\running-example.xes handover result_handover.png")
os.system("python -m pm4py.cli SaveVisSNA tests\\input_data\\running-example.xes working_together result_working_together.png")
os.system("python -m pm4py.cli SaveVisSNA tests\\input_data\\running-example.xes similar_activities result_similar_activities.png")
os.system("python -m pm4py.cli SaveVisSNA tests\\input_data\\running-example.xes subcontracting result_subcontracting.png")
os.system("python -m pm4py.cli SaveVisCaseDuration tests\\input_data\\running-example.xes result_case_duration.png")
os.system("python -m pm4py.cli FilterVariantsTopK tests\\input_data\\running-example.xes 1 result_filtering_top_k.xes")
os.system("python -m pm4py.cli FilterVariantsCoverage tests\\input_data\\running-example.xes 0.1 result_filtering_var_cov.xes")
os.system("python -m pm4py.cli FilterCasePerformance tests\\input_data\\running-example.xes 3600 86400 result_filtering_case_perf.xes")
os.system("python -m pm4py.cli FilterTimeRange tests\\input_data\\receipt.xes 2011-01-01 2011-01-31 result_filtering_time_range.xes")
