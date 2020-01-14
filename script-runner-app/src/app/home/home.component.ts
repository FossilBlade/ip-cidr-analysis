import {
  Component,
  OnInit,
  ChangeDetectionStrategy,
  ChangeDetectorRef,
  Input
} from "@angular/core";
import * as IPCIDR from "ip-cidr";
import { ApiService } from "../_services/api.service";

import { switchMap } from "rxjs/operators/switchMap";

import {
  HttpClient,
  HttpParams,
  HttpResponse,
  HttpEventType
} from "@angular/common/http";
import { saveAs as importedSaveAs } from "file-saver";
@Component({
  selector: "app-home",
  templateUrl: "./home.component.html",
  styleUrls: ["./home.component.scss"],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class HomeComponent implements OnInit {
  iserror: boolean = false;
  errormsg: string = "";
  checkresult: any;
  input_readonly: boolean = false;
  ip_cird: string = "";
  job_run_result: any;
  download_error: string;
  downloading: boolean;
  downloaded: boolean;
  download_prog: number = 0;

  constructor(private apiService: ApiService, private ref: ChangeDetectorRef) {}

  ngOnInit() {}

  onIpInputChange(event) {   

    this.iserror = false;
    this.errormsg = "";
    this.checkresult = null;
    this.input_readonly = false;
    this.ip_cird = "";
    this.job_run_result = null;
    this.download_error = null;
    this.downloading = false;
    this.downloaded = false;
    this.download_prog = 0;

    let temp_ip = event.target.value;
    if (!temp_ip) {
      this.iserror = false;
    } else if (event.keyCode == 13) {
      console.log("IP: " + temp_ip);
      this.input_readonly = true;
      this.ref.detectChanges();

      if (this.check_ip_valid(temp_ip)) {
        this.apiService.check_status_ip_cidr(temp_ip).subscribe(
          data => {
            this.checkresult = data;

            if (data.job_running) {
              console.error("JOB ALREADY RUNNING FOR IP: " + temp_ip);
              this.show_error("JOB ALREADY RUNNING FOR IP: " + temp_ip);
            }
            this.ip_cird = temp_ip;
            this.ref.detectChanges();
          },
          err => {
            console.log(typeof err);          

            this.show_error("Error: " + err);
            this.ref.detectChanges();
          }
        );
      } else {
        console.error("INVALID IP: " + temp_ip);
        this.show_error("INVALID IP: " + temp_ip);
      }
    }

    this.input_readonly = false;
    this.ref.detectChanges();
  }

  runJob() {
    this.input_readonly = true;
    this.ref.detectChanges();

    this.apiService.run_job(this.ip_cird).subscribe(
      data => {
        this.job_run_result = data;
        console.log(this.job_run_result);

        this.ref.detectChanges();
      },
      err => {
        console.log(typeof err);

        this.job_run_result = { error: err };
        this.ref.detectChanges();
      }
    );

    this.input_readonly = false;
  }

  show_error(msg: string) {
    this.iserror = true;
    this.errormsg = msg;
  }

  check_ip_valid(ip_cird) {
    try {
      console.log(ip_cird);
      const cidr = new IPCIDR(ip_cird);

      if (!cidr.isValid()) {
        return false;
      } else {
        return true;
      }
    } catch (err) {
      return false;
    }
  }

  downLoadFile(data: any, type: string) {
    this.input_readonly = true;
    this.ref.detectChanges();

    let blob = new Blob([data], { type: type });
    let url = window.URL.createObjectURL(blob);
    let pwa = window.open(url);

    if (!pwa || pwa.closed || typeof pwa.closed == "undefined") {
      alert("Please disable your Pop-up blocker and try again.");
    }

    this.input_readonly = false;
    this.ref.detectChanges();
  }

  download() {
    this.downloaded = false;
    this.ref.detectChanges();

    this.apiService
      .downloadFile(this.ip_cird, this.download_prog, this.ref)
      .subscribe(
        result => {
         

          if (result.type === HttpEventType.DownloadProgress) {
            this.downloading = true;

            const percentDone = Math.round(
              (100 * result.loaded) / result.total
            );
            this.download_prog = percentDone;
            console.log(this.download_prog);
          }
          if (result.type === HttpEventType.Response) {
            importedSaveAs(
              result.body,
              this.ip_cird.replace("/", "-") + "_report.txt"
            );
            this.downloading = false;
            this.downloaded = true;
          }

          this.ref.detectChanges();
        },
        err => {
          this.download_prog = null;
          this.download_error = err;
          this.downloading = false;
          this.downloaded = true;
          this.ref.detectChanges();
        }
      );
  }
}
