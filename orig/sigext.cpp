{
   gROOT->Reset();
   gROOT->SetStyle("Plain");
   gStyle->SetOptTitle(0);
   gStyle->SetOptStat(0);
   gStyle->SetFillColor(0);
   gStyle->SetPadBorderMode(0);
   m = (TH1F*)gROOT->FindObject("h");
   if (m) m->Delete();
   TCanvas *c1 = new TCanvas("c1","Normalization of gamma-transmission coefficient",600,600);
   TH2F *h = new TH2F("h"," ",10,-0.840000,   8.560,50,9.662e+00,1.599e+08);
   ifstream sigfile("sigpaw.cnt");
   float sig[72],sigerr[72];
   float energy[167],energyerr[167];
   float extL[168],extH[168];
   int i;
   float a0 = -0.8400;
   float a1 =  0.1200;
   for(i = 0; i < 73; i++){
   	energy[i] = a0 + (a1*i);
   	energyerr[i] = 0.0;
   	extL[i] = 0.0;
   	extH[i] = 0.0;
   }
   float x, y;
   i = 0;
   while(sigfile){
   	sigfile >> x;
   	if(i<71){
   		sig[i]=x;
   	}
   	else{sigerr[i-71]=x;}
   	i++;
   }
   ifstream extendfile("extendLH.cnt");
   i = 0;
   while(extendfile){
   	extendfile >> x >> y ;
   	extL[i]=x;
   	extH[i]=y;
   	i++;
   }
   TGraph *extLgraph = new TGraph(73,energy,extL);
   TGraph *extHgraph = new TGraph(73,energy,extH);
   TGraphErrors *sigexp = new TGraphErrors(71,energy,sig,energyerr,sigerr);
   c1->SetLogy();
   c1->SetLeftMargin(0.14);
   h->GetXaxis()->CenterTitle();
   h->GetXaxis()->SetTitle("#gamma-ray energy E_{#gamma} (MeV)");
   h->GetYaxis()->CenterTitle();
   h->GetYaxis()->SetTitleOffset(1.4);
   h->GetYaxis()->SetTitle("Transmission coeff. (arb. units)");
   h->Draw();
   sigexp->SetMarkerStyle(21);
   sigexp->SetMarkerSize(0.8);
   sigexp->Draw("P");
   extLgraph->SetLineStyle(1);
   extLgraph->DrawGraph(22,&extLgraph->GetX()[0],&extLgraph->GetY()[0],"L");
   extHgraph->SetLineStyle(1);
   extHgraph->DrawGraph(16,&extHgraph->GetX()[57],&extHgraph->GetY()[57],"L");
   TArrow *arrow1 = new TArrow(1.320e+00,9.425e+03,1.320e+00,1.425e+03,0.02,">");
   arrow1->Draw();
   TArrow *arrow2 = new TArrow(1.680e+00,2.774e+04,1.680e+00,4.194e+03,0.02,">");
   arrow2->Draw();
   TArrow *arrow3 = new TArrow(6.000e+00,1.018e+07,6.000e+00,1.539e+06,0.02,">");
   arrow3->Draw();
   TArrow *arrow4 = new TArrow(6.960e+00,5.717e+07,6.960e+00,8.646e+06,0.02,">");
   arrow4->Draw();
   c1->Update();
   c1->Print("sigext.pdf");
   c1->Print("sigext.eps");
   c1->Print("sigext.ps");
}
