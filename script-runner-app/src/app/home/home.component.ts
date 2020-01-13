import { Component, OnInit, ChangeDetectionStrategy } from "@angular/core";
import * as IPCIDR from "ip-cidr";

@Component({
  selector: "app-home",
  templateUrl: "./home.component.html",
  styleUrls: ["./home.component.scss"],
  changeDetection: ChangeDetectionStrategy.Default
})
export class HomeComponent implements OnInit {
  ip_cidr: string;
  valid_ip_cidr: boolean = false;
  btn_pressed: boolean = false;

  constructor() {}

  ngOnInit() {}

  onKey(event) {
    let temp = event.target.value;

    const cidr = new IPCIDR(temp);

    if (!cidr.isValid()) {
      this.valid_ip_cidr = false;
    } else {
      this.valid_ip_cidr = true;
    }


  }

  onClick() {
    
  }
}
