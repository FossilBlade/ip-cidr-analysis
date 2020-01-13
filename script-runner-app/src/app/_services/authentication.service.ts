import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';


import { environment } from '../../environments/environment';
import { User } from '../_models/user';

import { switchMap } from 'rxjs/operators/switchMap';
import { finalize } from 'rxjs/operators/finalize';
import { timeout } from 'rxjs/operators/timeout';
import { catchError } from 'rxjs/operators/catchError';
import { _throw } from 'rxjs/observable/throw';
import { retry } from 'rxjs/operators/retry';
import { of } from 'rxjs/observable/of';
import { map } from 'rxjs/operators';
@Injectable({ providedIn: 'root' })
export class AuthenticationService {
    private currentUserSubject: BehaviorSubject<String>;
    public currentUser: Observable<String>;

    constructor(private http: HttpClient) {
        this.currentUserSubject = new BehaviorSubject<String>(JSON.parse(localStorage.getItem('jwt')));
        this.currentUser = this.currentUserSubject.asObservable();
    }

    public get currentUserValue(): String {
        return this.currentUserSubject.value;
    }

    login(username: string, password: string) {
        return this.http.post<any>(`${environment.apiUrl}/auth`, { username, password })
            .pipe(timeout(1000),retry(1),
                catchError((e, c) => { return _throw(e) }),
                switchMap(authToken => {
                    console.log('do something with ' + JSON.stringify(authToken));


                    // store user details and basic auth credentials in local storage to keep user logged in between page refreshes
                    // user.authdata = window.btoa(username + ':' + password);
                    localStorage.setItem('jwt', JSON.stringify(authToken.access_token));
                    this.currentUserSubject.next(authToken.access_token);
                    // return user;


                    return of(authToken.token)
                }),
                finalize(() => { console.log('finilize') })

            )
    }

    logout() {
        // remove user from local storage to log user out
        localStorage.removeItem('jwt');
        this.currentUserSubject.next(null);
    }
}