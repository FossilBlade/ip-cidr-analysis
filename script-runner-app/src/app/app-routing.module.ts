import { NgModule } from '@angular/core';

import { Routes, RouterModule } from '@angular/router';

import {AuthGuard} from './_helpers/auth.guard';

const routes: Routes = [
  { path: '', loadChildren: './home/home.module#HomeModule', canActivate: [AuthGuard] },
  { path: 'login', loadChildren: './login/login.module#LoginModule'},
  { path: '**', redirectTo: '' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule { }
