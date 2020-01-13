import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NbCardModule, NbInputModule, NbButtonModule, NbIconModule, NbSpinnerModule,NbAlertModule } from '@nebular/theme';
import { FormsModule } from '@angular/forms';

@NgModule({
  declarations: [],
  imports: [
    CommonModule,
    NbCardModule,
    NbInputModule,
    NbButtonModule,
    NbIconModule,
    NbSpinnerModule,
    NbAlertModule,
    FormsModule
  ],
  exports: [NbCardModule, NbInputModule, NbButtonModule, NbIconModule, NbSpinnerModule,NbAlertModule,FormsModule]
})
export class SharedModule { }
