import {
  Component,
  OnInit,
  ChangeDetectionStrategy,
  ChangeDetectorRef,
  Input
} from "@angular/core";
import * as IPCIDR from "ip-cidr";
import { ApiService } from "../_services/api.service";

@Component({
  selector: "app-home",
  templateUrl: "./home.component.html",
  styleUrls: ["./home.component.scss"],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class HomeComponent implements OnInit {
  
  iserror: boolean = false; 
  errormsg: string = ""; 
  data: any;  
  input_readonly: boolean = false;

  constructor(
    private apinService: ApiService,
    private ref: ChangeDetectorRef
  ) {}

  ngOnInit() {}

  onIpInputChange(event) {
    this.iserror = false;
    this.data = null;
   

    let ip_cidr = event.target.value;
    if (!ip_cidr) {
      this.iserror = false;
    } else if (event.keyCode == 13) {
      console.log("IP: " + ip_cidr);
      this.input_readonly=true;
      this.ref.detectChanges()

      if (this.check_ip_valid(ip_cidr)) {
        this.apinService.check_status_ip_cidr(ip_cidr).subscribe(data => {
          this.data = data;

          if (data.job_running) {
            console.error("JOB ALREADY RUNNING FOR IP: " + ip_cidr);
            this.show_error("JOB ALREADY RUNNING FOR IP: " + ip_cidr);
          } 
          this.ref.detectChanges()
        });
      } else {
        console.error("INVALID IP: " + ip_cidr);
        this.show_error("INVALID IP: " + ip_cidr);
      }
      
    }
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
}
