import { Injectable } from "@angular/core";
import {
  HttpClient,
  HttpParams,
  HttpResponse,
  HttpEventType
} from "@angular/common/http";
import { ResponseContentType } from "@angular/http";
import { saveAs as importedSaveAs } from "file-saver";

import { environment } from "../../environments/environment";
import { CheckResult } from "../_models/check-result";

import { switchMap } from "rxjs/operators/switchMap";
import { finalize } from "rxjs/operators/finalize";
import { timeout } from "rxjs/operators/timeout";
import { catchError } from "rxjs/operators/catchError";
import { _throw } from "rxjs/observable/throw";
import { retry } from "rxjs/operators/retry";
import { of } from "rxjs/observable/of";
import { map } from "rxjs/operators";
@Injectable({ providedIn: "root" })
export class ApiService {
  constructor(private http: HttpClient) {}

  check_status_ip_cidr(ipcidr: string) {
    let params = new HttpParams().set("ipcidr", ipcidr);

    return this.http
      .get<CheckResult>(`${environment.apiUrl}/check`, { params: params })
      .pipe(
        timeout(5000),
        retry(0),
        catchError((e, c) => {
          return _throw(e);
        }),
        switchMap(resp => {
          console.log("Response Recieved: " + JSON.stringify(resp));

          return of(resp);
        }),
        finalize(() => {
          console.log("finilize");
        })
      );
  }

  run_job(ipcidr: string) {
    let params = new HttpParams().set("ipcidr", ipcidr);

    return this.http
      .get<any>(`${environment.apiUrl}/job`, { params: params })
      .pipe(
        timeout(5000),
        retry(0),
        catchError((e, c) => {
          return _throw(e);
        }),
        switchMap(resp => {
          console.log("Response Recieved: " + JSON.stringify(resp));

          return of(resp);
        }),
        finalize(() => {
          console.log("finilize");
        })
      );
  }

  downloadFile(ipcidr: string, progressbar: number, changePusher): any {
    let params = new HttpParams().set("ipcidr", ipcidr);

    return this.http.get(`${environment.apiUrl}/report`, {
      params: params,
      responseType: "blob",
      reportProgress: true,
      observe: "events"
    });
  }
}
