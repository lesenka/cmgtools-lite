from PhysicsTools.Heppy.analyzers.core.AutoFillTreeProducer  import * 
from CMGTools.TTHAnalysis.analyzers.ntupleTypes  import *
from CMGTools.TTHAnalysis.analyzers.ntupleTypes  import *

hnl_globalVariables = [
            NTupleVariable("lheHT", lambda ev : getattr(ev,"lheHT",-999), mcOnly=True, help="H_{T} computed from quarks and gluons in Heppy LHEAnalyzer"),

            NTupleVariable("Flag_badMuonMoriond2017",  lambda ev: ev.badMuonMoriond2017, int, help="bad muon found in event (Moriond 2017 filter)?"),
            NTupleVariable("Flag_badCloneMuonMoriond2017",  lambda ev: ev.badCloneMuonMoriond2017, int, help="clone muon found in event (Moriond 2017 filter)?"),
            NTupleVariable("badCloneMuonMoriond2017_maxPt",  lambda ev: max(mu.pt() for mu in ev.badCloneMuonMoriond2017_badMuons) if not ev.badCloneMuonMoriond2017 else 0, help="max pt of any clone muon found in event (Moriond 2017 filter)"),
            NTupleVariable("badNotCloneMuonMoriond2017_maxPt",  lambda ev: max((mu.pt() if mu not in ev.badCloneMuonMoriond2017_badMuons else 0) for mu in ev.badMuonMoriond2017_badMuons) if not ev.badMuonMoriond2017 else 0, help="max pt of any bad non-clone muon found in event (Moriond 2017 filter)"),

            NTupleVariable("rho",  lambda ev: ev.rho, float, help="kt6PFJets rho"),
            NTupleVariable("rhoCN",  lambda ev: ev.rhoCN, float, help="fixed grid rho central neutral"),
            NTupleVariable("nVert",  lambda ev: len(ev.goodVertices), int, help="Number of good vertices"), 

]

hnl_globalObjects = {
            "met" : NTupleObject("met", metType, help="PF E_{T}^{miss}, after type 1 corrections"),
}

hnl_collections = {
            "generatorSummary" : NTupleCollection("GenPart", genParticleWithLinksType, 100 , help="Hard scattering particles, with ancestry and links"),
            "selectedLeptons" : NTupleCollection("LepGood",  leptonTypeSusyExtra, 8, help="Leptons after the preselection"),
            "cleanJets"       : NTupleCollection("Jet",     jetTypeExtra, 15, help="Cental jets after full selection and cleaning, sorted by pt"),
            "ivf"       : NTupleCollection("SV",     svType, 20, help="SVs from IVF"),
            "LHE_weights"    : NTupleCollection("LHEweight",  weightsInfoType, 1000, mcOnly=True, help="LHE weight info"),

}
