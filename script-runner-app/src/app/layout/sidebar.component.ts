import { Component } from '@angular/core';
import { NbMenuItem } from '@nebular/theme';

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
})
export class SidebarComponent {

  menuItems: NbMenuItem[] = [
    {
      title: 'Home',
      link: '/home',
      children: null
    },
    {
      title: 'Login',
      link: '/Login',
      children: null
    }
  ];

}
