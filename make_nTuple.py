## Warning ##
## This code designed at a hybrid conda-environment! ##
## If you want to contact the code designer, please visit ROOM 208 and call Tau Kim ##

import uproot as ROOT
import vector
import numpy as np
import glob
import awkward as ak
from coffea import nanoevents
from coffea import lumi_tools

######################## FUNCTION DEFINITION ############################

def myReader(filepath):
	targetPattern = r""+ filepath +""
	allfiles = glob.glob(targetPattern)
	filelist = []
	openlist = []
	for f in allfiles:
		filelist.append(f)
		openlist.append(f+ ':Events')

	return filelist, openlist



def tupleMaker(filepath, filetype, DATA=False):
	## Get file list
	print("Start of",filetype)

	filelist, openlist = myReader(filepath)

	branches = ['MET_pt','nElectron','nMuon','nJet','run','luminosityBlock']

	histo = {}
	count = 0
	## Fileloop
	for arrays, doc in ROOT.iterate(openlist,branches,report=True):
		print("from: {0}, to: {1} -- Entries: {2}".format(doc.start,doc.stop,len(arrays)))
		
		MET = arrays[b"MET_pt"]
		nElectron = arrays[b"nElectron"]
		nMuon = arrays[b"nMuon"]
		nJet = arrays[b"nJet"]
		
		RUN = arrays[b"run"]
		LumiBlock = arrays[b"luminosityBlock"]

		### GOLDEN JSON
		if DATA == True:
			injson="Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt" ## input your golden json filepath
			lumi_mask_builder = lumi_tools.LumiMask(injson)
			lumimask = ak.Array(lumi_mask_builder.__call__(RUN,LumiBlock))

			### DATA REDUCTION
			MET = MET[lumimask]
			nElectron = nElectron[lumimask]
			nMuon = nMuon[lumimask]
			nJet = nJet[lumimask]

			print("Good run events ratio = {0} %".format(len(MET)/len(arrays)*100))


		### Append and Concatenate
		if len(histo) == 0:
			histo['MET'] = MET
			histo['nElectron'] = nElectron
			histo['nMuon'] = nMuon
			histo['nJet'] = nJet
		else:
			histo['MET'] = np.concatenate((histo['MET'],MET))
			histo['nElectron'] = np.concatenate((histo['nElectron'],nElectron))
			histo['nMuon'] = np.concatenate((histo['nMuon'],nMuon))
			histo['nJet'] = np.concatenate((histo['nJet'],nJet))

	## Save nTuple
	np.save(""+ folder +"/"+ filetype +"_nTuple",histo)
	## EOF

######################## FUNCTION DEFINITION ############################



######################## MAIN CODE START ################################
folder = "DATA_SKIMMING"


### DATA
pathlist = [
"/x6/cms/store/data/Run2018A/MET/NANOAOD/UL2018_MiniAODv2_NanoAODv9-v2/*/*.root",
"/x6/cms/store/data/Run2018B/MET/NANOAOD/UL2018_MiniAODv2_NanoAODv9-v2/*/*.root",
"/x6/cms/store/data/Run2018C/MET/NANOAOD/UL2018_MiniAODv2_NanoAODv9-v1/*/*.root",
"/x6/cms/store/data/Run2018D/MET/NANOAOD/UL2018_MiniAODv2_NanoAODv9-v1/*/*.root"
]

labellist = ['Run2018A','Run2018B','Run2018C','Run2018D']

### DATALOOP
for i in range(len(pathlist)):
	tupleMaker(pathlist[i],labellist[i],DATA=True)


### MC
pathlist = [
"/x6/cms/store/mc/RunIISummer20UL18NanoAODv9/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/FSUL18_FSUL18_106X_upgrade2018_realistic_v16_L1v1_ext1-v3/*/*.root",
"/x6/cms/store/mc/RunIISummer20UL18NanoAODv9/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/*/*.root",
"/x6/cms/store/mc/RunIISummer20UL18NanoAODv9/TTZToNuNu_TuneCP5_13TeV-amcatnlo-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/*/*.root",
"/x6/cms/store/mc/RunIISummer20UL18NanoAODv9/WW_TuneCP5_13TeV-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/*/*.root",
"/x6/cms/store/mc/RunIISummer20UL18NanoAODv9/WZ_TuneCP5_13TeV-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/*/*.root",
"/x6/cms/store/mc/RunIISummer20UL18NanoAODv9/TTToSemileptonic_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/FSUL18_FSUL18_106X_upgrade2018_realistic_v16_L1v1_ext1-v3/*/*.root",
"/x6/cms/store/mc/RunIISummer20UL18NanoAODv9/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/*/*.root",
"/x6/cms/store/mc/RunIISummer20UL18NanoAODv9/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/*/*.root"
]

labellist = ['TTTo2L2Nu_UL18','TTWJetsToLNu_UL18','TTZToNuNu_UL18','WW_UL18','WZ_UL18','TTToSemileptonic_UL18','ST_TW_top_UL18','ST_TW_anti_UL18']

### MCLOOP

for i in range(len(pathlist)):
	tupleMaker(pathlist[i],labellist[i],DATA=False)


######################## END OF CODE ###########################
