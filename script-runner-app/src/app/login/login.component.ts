import { Component, OnInit, ChangeDetectionStrategy } from '@angular/core';
// import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';
import { AuthenticationService } from '../_services/authentication.service';
import { first } from 'rxjs/operators';

import { ChangeDetectorRef } from '@angular/core'

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class LoginComponent implements OnInit {

  loading = false;
  returnUrl: string;
  error = '';
  username: string;
  password: string;


  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private authenticationService: AuthenticationService, private ref: ChangeDetectorRef
  ) {
    // redirect to home if already logged in
    if (this.authenticationService.currentUserValue) {
      this.router.navigate(['/']);
    }
  }

  ngOnInit() {

    // get return url from route parameters or default to '/'
    this.returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/';
  }

  onSubmit() {

    this.loading = true;

    this.authenticationService.login(this.username, this.password)
      .subscribe(data => {
        this.router.navigate([this.returnUrl]);
      }, err => {

        if (err == 'TimeoutError') {
          this.error = 'Login Request Timed Out';
        }
        else {

          this.error = ' Unknown Error: ' + err;

        }
        this.loading = false;
        this.ref.detectChanges()

      });    
  }
}
