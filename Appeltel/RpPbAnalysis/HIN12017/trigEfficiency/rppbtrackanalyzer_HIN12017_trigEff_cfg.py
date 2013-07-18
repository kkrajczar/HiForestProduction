import FWCore.ParameterSet.Config as cms

process = cms.Process('TRACKANA')
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
#process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('Configuration.StandardSequences.ReconstructionHeavyIons_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
#process.load('Configuration.EventContent.EventContentHeavyIons_cff')
process.load('Appeltel.RpPbAnalysis.RpPbTrackingAnalyzer_cff')
process.load('HeavyIonsAnalysis.Configuration.collisionEventSelection_cff')


process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(3)
)

process.TFileService = cms.Service("TFileService",
    fileName = cms.string('trackAnalysis.root')
)

from HeavyIonsAnalysis.Configuration.CommonFunctions_cff import *
overrideCentrality(process)

process.HeavyIonGlobalParameters = cms.PSet(
  centralityVariable = cms.string("HFtowersPlusTrunc"),
  nonDefaultGlauberModel = cms.string("Hijing"),
  centralitySrc = cms.InputTag("pACentrality"),
  pPbRunFlip = cms.untracked.uint32(99999999)
  )


# Input source
process.source = cms.Source("PoolSource",
    duplicateCheckMode = cms.untracked.string("noDuplicateCheck"),
    fileNames =  cms.untracked.vstring(
#'file:/scratch/appelte1/HIJING_mix_Dijet120_1000ev.root'
'/store/himc/HiWinter13/Hijing_PPb502_MinimumBias/GEN-SIM-RECO/pa_STARTHI53_V25-v1/20000/B09F0E3E-4576-E211-8D3B-0026B94D1ABB.root'
    )
)

# JETS

process.load('CmsHi.JetAnalysis.ExtraPfReco_cff')
process.load('CmsHi.JetAnalysis.ExtraJetReco_cff')
process.load('CmsHi.JetAnalysis.PatAna_cff')
process.PFTowers.src = cms.InputTag("particleFlow")

process.load("HLTrigger.HLTfilters.hltHighLevel_cfi")
process.hltSingleTrigger = process.hltHighLevel.clone()
process.hltSingleTrigger.HLTPaths = ["HLT_PAZeroBiasPixel_SingleTrack_v1"]

process.GlobalTag.globaltag = 'STARTHI53_V25::All'

process.trkAna_HIN12017_MC.doTrigEffCorrection = cms.bool(False)
process.trkAna_HIN12017_MC_noSel = process.trkAna_HIN12017_MC.clone()

process.jetReco= cms.Sequence(
    process.PFTowers *
    process.akPu3PFJets*
    process.akPu3PFcorr*
    process.akPu3PFpatJets*
    process.akPu3CaloJets*
    process.akPu3CaloJetID*
    process.akPu3Calocorr*
    process.akPu3CalopatJets
)

process.p = cms.Path( 
    process.siPixelRecHits *
    process.pACentrality *
    process.jetReco *
    process.genParticles *
    process.trkAna_HIN12017_MC_noSel *
    process.PAcollisionEventSelection * 
    process.hltSingleTrigger *
    process.trkAna_HIN12017_MC 
)

