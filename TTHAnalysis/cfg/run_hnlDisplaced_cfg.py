

##########################################################
##       CONFIGURATION FOR HNL TREES                    ##
## skim condition: >= 2 loose leptons, no pt cuts or id ##
##########################################################
import PhysicsTools.HeppyCore.framework.config as cfg
import re

#-------- LOAD ALL ANALYZERS -----------

from CMGTools.TTHAnalysis.analyzers.susyCore_modules_cff import *
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption

susyCoreSequence.remove(genHiggsAna)
susyCoreSequence.remove(genHFAna)
susyCoreSequence.remove(pdfwAna)
susyCoreSequence.remove(susyScanAna)
susyCoreSequence.remove(tauAna)
susyCoreSequence.remove(photonAna)
susyCoreSequence.remove(isoTrackAna)

#-------- SET OPTIONS AND REDEFINE CONFIGURATIONS -----------
isTest = getHeppyOption("test",None) != None and not re.match("^\d+$",getHeppyOption("test"))

# Lepton Skimming
ttHLepSkim.minLeptons = 3
ttHLepSkim.maxLeptons = 999

# Run miniIso
lepAna.doMiniIsolation = True
lepAna.packedCandidates = 'packedPFCandidates'
lepAna.miniIsolationPUCorr = 'rhoArea'
lepAna.miniIsolationVetoLeptons = None # use 'inclusive' to veto inclusive leptons and their footprint in all isolation cones
lepAna.doIsolationScan = False

# Lepton Preselection
# inclusive very loose muon selection
lepAna.inclusive_muon_pt = 5
lepAna.inclusive_muon_dxy = 99999
lepAna.inclusive_muon_dz = 99999
# loose muon selection
lepAna.loose_muon_dxy = 99999
lepAna.loose_muon_dz = 99999
lepAna.loose_muon_relIso = 1.0

# inclusive very loose electron selection
lepAna.inclusive_electron_id  = ""
lepAna.inclusive_electron_pt  = 5
lepAna.inclusive_electron_eta = 2.5
lepAna.inclusive_electron_dxy = 99999
lepAna.inclusive_electron_dz  = 99999
lepAna.inclusive_electron_lostHits = 10.0,
# loose electron selection
lepAna.loose_electron_id     = ""
lepAna.loose_electron_pt     = 5,
lepAna.loose_electron_eta    = 2.5,
lepAna.loose_electron_dxy    = 99999,
lepAna.loose_electron_dz     = 99999,
lepAna.loose_electron_relIso = 1.0,
lepAna.loose_electron_lostHits = 10.0,

jetAna.copyJetsByValue = True # do not remove this
metAna.copyMETsByValue = True # do not remove this

jetAna.cleanJetsFromLeptons=False
jetAna.cleanSelectedLeptons=False
jetAna.storeLowPtJets=False
jetAna.jetEtaCentral = jetAna.jetEta
jetAna.mcGT="Spring16_25nsV8_MC"
jetAna.dataGT   = "Spring16_25nsV8BCD_DATA Spring16_25nsV8E_DATA Spring16_25nsV8F_DATA Spring16_25nsV8_DATA"
jetAna.runsDataJEC   = [276811, 277420, 278802]

susyCoreSequence.insert(susyCoreSequence.index(ttHCoreEventAna),
                        ttHSVAna)

## tree configuration
from CMGTools.TTHAnalysis.analyzers.treeProducerHNL import *

susyCoreSequence.insert(susyCoreSequence.index(ttHCoreEventAna),
                        susyLeptonMatchAna)
leptonTypeSusyExtraLight.addVariables([
                                      NTupleVariable("mcUCSXMatchId", lambda x : x.mcUCSXMatchId if hasattr(x,'mcUCSXMatchId') else -1, mcOnly=True, help="MC truth matching a la UCSX"),
                                                                   ])
leptonTypeSusy.addVariables([
                             NTupleVariable("mvaIdSpring16HZZ",   lambda lepton : lepton.mvaRun2("Spring16HZZ") if abs(lepton.pdgId()) == 11 else 1, help="EGamma POG MVA ID, Spring16, HZZ; 1 for muons"),
                             NTupleVariable("mvaIdSpring16GP",   lambda lepton : lepton.mvaRun2("Spring16GP") if abs(lepton.pdgId()) == 11 else 1, help="EGamma POG MVA ID, Spring16, GeneralPurpose; 1 for muons"),
                             ])

## Tree Producer
treeProducer = cfg.Analyzer(
                            AutoFillTreeProducer, name='treeProducerHNL',
                            vectorTree = True,
                            saveTLorentzVectors = False,  # can set to True to get also the TLorentzVectors, but trees will be bigger
                            defaultFloatType = 'F', # use Float_t for floating point
                            globalVariables = hnl_globalVariables,
                            globalObjects = hnl_globalObjects,
                            collections = hnl_collections,
                            )

from CMGTools.RootTools.samples.samples_13TeV_RunIISummer16MiniAODv2 import *
#from CMGTools.RootTools.samples.samples_13TeV_DATA2016 import *
from CMGTools.HToZZ4L.tools.configTools import printSummary, configureSplittingFromTime, cropToLumi, prescaleComponents, insertEventSelector

selectedComponents = [TTLep_pow]


#-------- SEQUENCE -----------

sequence = cfg.Sequence(susyCoreSequence+[
                                          treeProducer,
                                          ])
preprocessor = None

#-------- HOW TO RUN -----------

test = getHeppyOption('test')
if test == '1':
    #comp = selectedComponents[0]
    comp = cfg.MCComponent( files = ["/afs/cern.ch/work/m/mvit/public/HeavyNeutrino_trilepton_M-40_V-1e-05_2l_NLO/heavyNeutrino_100.root"], name="M-40_V-1e-05_2l_NLO" )
    comp.files = comp.files[:1]
    comp.splitFactor = 1
    comp.fineSplitFactor = 1
    selectedComponents = [ comp ]

## Auto-AAA
from CMGTools.RootTools.samples.autoAAAconfig import *
if not getHeppyOption("isCrab"):
    autoAAA(selectedComponents)

## output histogram
outputService=[]
from PhysicsTools.HeppyCore.framework.services.tfile import TFileService
output_service = cfg.Service(
                             TFileService,
                             'outputfile',
                             name="outputfile",
                             fname='treeProducerHNL/tree.root',
                             option='recreate'
                             )    
outputService.append(output_service)

# print summary of components to process
printSummary(selectedComponents)

# the following is declared in case this cfg is used in input to the heppy.py script
from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
from CMGTools.TTHAnalysis.tools.EOSEventsWithDownload import EOSEventsWithDownload
event_class = EOSEventsWithDownload if not preprocessor else Events
EOSEventsWithDownload.aggressive = 2 # always fetch if running on Wigner
if getHeppyOption("nofetch") or getHeppyOption("isCrab"):
    event_class = Events
    if preprocessor: preprocessor.prefetch = False
config = cfg.Config( components = selectedComponents,
                    sequence = sequence,
                    services = outputService,
                    preprocessor = preprocessor,
                    events_class = event_class)



