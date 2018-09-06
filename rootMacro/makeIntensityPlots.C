void makeIntensityPlots(float Eth, float dt) {

    TFile file("root/60h_ROOT_Tree.root");
    TCanvas c;
    TTree* tree = (TTree*) file.Get("FastRotation/frTree");

    float time_;
    int caloNum_;
    int bunchNum_;
    float energy_;
    tree->SetBranchAddress("time",&time_);
    tree->SetBranchAddress("caloNum",&caloNum_);
    tree->SetBranchAddress("bunchNum",&bunchNum_);
    tree->SetBranchAddress("energy",&energy_);
    unsigned int nEntries = tree->GetEntries();


    std::array<TH1F*, 8> h_perCaloPerBunch[24];
    TH1F* h_perCaloAllBunch[24];
    TH1F* h_allCalosPerBunch[8];
    TH1F* h_allCalosallBunches = new TH1F ("allCalosallBunches_intensitySpectrum","allCalosallBunches_intensitySpectrum", 596000, 0, 596);

    TString string;

    for(int iCalo = 0 ; iCalo <24; ++iCalo){

        string = Form("calo%d_intensitySpectrum", iCalo+1);
        h_perCaloAllBunch[iCalo] =  new TH1F (string, string, 596000, 0, 596); // to be able to divide by 149
        h_perCaloAllBunch[iCalo] -> GetXaxis() -> SetTitle ("Time [#mus]");
        h_perCaloAllBunch[iCalo] -> GetYaxis() -> SetTitle ("#");

        for(int iBunch = 0; iBunch < 8; ++iBunch){
            string = Form("calo%dBunch%d_intensitySpectrum", iCalo, iBunch);
            h_perCaloPerBunch[iCalo][iBunch] =  new TH1F (string, string, 596000, 0, 596);
            h_perCaloPerBunch[iCalo][iBunch] -> GetXaxis() -> SetTitle ("Time [#muns]");
            h_perCaloPerBunch[iCalo][iBunch] -> GetYaxis() -> SetTitle ("#");
        }

    }

    for(int iBunch = 0; iBunch < 8; ++iBunch){
        string = Form("allCalosBunch%d_intensitySpectrum", iBunch);
        h_allCalosPerBunch[iBunch] =  new TH1F (string, string, 596000, 0, 596);
        h_allCalosPerBunch[iBunch] -> GetXaxis() -> SetTitle ("Time [#mus]");
        h_allCalosPerBunch[iBunch] -> GetYaxis() -> SetTitle ("#");
    }


//    for ( unsigned int i=0; i<100000; ++i ) {
    for ( unsigned int i=0; i<nEntries; ++i ) {
        tree->GetEntry( i );
        if ( energy_ > Eth) {
            h_perCaloAllBunch[caloNum_-1]               -> Fill ( 0.001 * 1.25 * time_ );
            h_perCaloPerBunch[caloNum_-1][bunchNum_]    -> Fill ( 0.001 * 1.25 * time_ );
            h_allCalosPerBunch[bunchNum_]               -> Fill( 0.001 * ( 1.25*time_ - dt*(caloNum_-1) ) );
            h_allCalosallBunches                        -> Fill( 0.001 * ( 1.25*time_ - dt*(caloNum_-1) ) );

        }
    }

    TFile oFile( Form("root/IntensitySpectrum_60h_Eth_%.0f_dt_%.3f.root", Eth, dt), "RECREATE");

    h_allCalosallBunches -> Write();

    for(int iBunch = 0; iBunch < 8; ++iBunch){

        h_allCalosPerBunch[iBunch] -> Write();

    }

    for(int iCalo = 0 ; iCalo <24; ++iCalo){

        h_perCaloAllBunch[iCalo]->Write();

        for(int iBunch = 0; iBunch < 8; ++iBunch){

            h_perCaloPerBunch[iCalo][iBunch] -> Write();

        }
    }

}
