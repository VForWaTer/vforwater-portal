import { TestBed, inject } from '@angular/core/testing';

import { WpsService } from './wps.service';

xdescribe('WpsService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [WpsService]
    });
  });

  it('should be created', inject([WpsService], (service: WpsService) => {
    expect(service).toBeTruthy();
  }));
});
