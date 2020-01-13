import { ChangeDetectionStrategy, Component } from '@angular/core';
import { NbSidebarService } from '@nebular/theme';

@Component({
  selector: 'app-sidebar-toggle',
  changeDetection: ChangeDetectionStrategy.OnPush,
  styleUrls: ['./sidebar-toggle.component.scss'],
  template: `
    <button nbButton ghost (click)="toggle()"><nb-icon icon="menu"></nb-icon></button>
  `,
})
export class SidebarToggleComponent {

  constructor(private sidebarService: NbSidebarService) {
  }

  toggle() {
    this.sidebarService.toggle(false);
    return false;
  }
}
