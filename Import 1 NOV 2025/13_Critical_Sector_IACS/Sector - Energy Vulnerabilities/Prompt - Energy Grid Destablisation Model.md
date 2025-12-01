**Conceptual Simulation: The Iberian Peninsula Blackout (April 28, 2025)**

**Objective:** To create an interactive, educational tool that visualizes the causes, cascading effects, and impacts of a large-scale power outage, using the hypothetical Iberian Peninsula Blackout as a case study. The simulation would aim to demonstrate key learnings regarding grid stability with high Inverter-Based Resource (IBR) penetration, the importance of interconnection capacity, and the role of advanced IBR control modes.

**Core Technologies (Conceptual Usage):**

- **Three.js:** This library would be fundamental for rendering the 3D map of the Iberian Peninsula (Spain and Portugal). It could display terrain, and overlay geographical data like city locations, power plants, substations, and transmission lines.[[6](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXFAvkwTbAy-XT2dvaAMvAQGlpSlkLD1pzjYTAgR9wgfSwrVIx26aOQ6J9KgaSEDe804060gdcJTvMaisZ2tUuut_zZDPDwiCwAg8m_Y8Dkcvcvmmimvi2oEXkc%3D)][[7](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXFdcle35UvhaHEeDUmZQS9T169O5zGEnnosHp4FsbT5IySoP4W4WpWBGM1G51NbDmokZuh_J9e2NWNKPABSg-dccjB2KGS-pefSaSmPxExpDOplJcbHIWY-1FHlrWvvl3ZQd7Y%3D)][[8](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXHAsLCI1oIgRpe1y_J270kTh5lwJG7kCZBken0H06md4w9m-Qv2eayqDjzUAl4zYyjJ9iir56iM5x-ocFRxaaEcc-Ad_AAKSgWTfInQ3qbVMomDPt7lGo0GhiqutQ%3D%3D)][[9](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXFjEZbq3sXboB5YJaX7iOn1ukMMYJY4QRAaFPYiuG9STpCxXfTmzDtwBMLVK8RcUZLRS7UzmkYWduIHjhTXeKuVtoj3MPEsB_GvBQANSkkGf1HZ7gWYzGMJUJUgj6WbmyFCATvf4synvEmedcGKq1OZwIPh65tDfXhGOjmH)][[10](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXHlzLaHUbSTuj8_lIdqBfEubWI7x6yHdJSroXEyJOMdeMMERQw94sG7YoydHkU956wK5qPxQJbO68Rfe_LQadf-A-u8MFsjNPi0TvGK-952nHhIRrIeLjkEIoCkdHUai-XcHtYaTdlXduyvGauz0g7BCaDU3OY3JAU1nMbxBCeV-BvdTUK7u1wu_i_TKUyKUb2x)] Libraries like geo-three or three-geo could be leveraged for map tiling and DEM (Digital Elevation Model) integration to create realistic terrain.[[6](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXFAvkwTbAy-XT2dvaAMvAQGlpSlkLD1pzjYTAgR9wgfSwrVIx26aOQ6J9KgaSEDe804060gdcJTvMaisZ2tUuut_zZDPDwiCwAg8m_Y8Dkcvcvmmimvi2oEXkc%3D)][[8](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXHAsLCI1oIgRpe1y_J270kTh5lwJG7kCZBken0H06md4w9m-Qv2eayqDjzUAl4zYyjJ9iir56iM5x-ocFRxaaEcc-Ad_AAKSgWTfInQ3qbVMomDPt7lGo0GhiqutQ%3D%3D)]
    
- **Anime.js:** This lightweight JavaScript animation library would be used to bring the simulation to life.[[11](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXG9_V-UokpG4qM2ACbqiD3DM5550bAwyTdqviaqtUNI2S3LBOuSo1hWD91NuCv6ePGn2HDB8zvA9gt2yYNqGXUEgyGWME7xZOSywle0jkXuJUJ-zhUz2NfWQ4E5WXG0fKvN7pWLV_IwSFv7dNjzpV__G74-2QKx1DttdH_AU6c%3D)][[12](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXEjOSs00F4rl6hwF4R1gEZPLLr5IzQ_Vdlf-ny8X-py65EBTZTuztGXVy39Ttdjeyy9gjxcxifBOnjBrn_tKYPPoLMLILSn0kxoi0B_BJLEqE7cCF2njp7jpViD-unv2z3KHa1OR8XKnchaSpE8PsPZIM5XXbSPwTyB)][[13](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXF5PrUVSd04seVyC9phsbTCBSHMtB9CkvEAZYPP2Tx_ODwa5ayPkZrTniQ1ip-BknKLhs3p97Ptit_CQvxhgr-uxBGh6B3_yL5HIltQnuFaxz3I1S7ICHq6Eb5mDuEMLsHWJInXlX3QeXoeRxegJqND)][[14](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXGBrue9euig399W4I80TW_iZARKOkkjerEQHHCN7Ujh3lNIe25-aZJKsWedh0AAFoH-_VxvCm-TqfvuiM_Yqt5PMgXj6RDQdFJ6DrzyaIAfj2THzqWYVm6eeqqNuwzwKxHtDbm3hkuj553eGnT4bkOAUuSTFSLFYvsCN8eycIrSUQkgCSjfZA%3D%3D)][[15](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXECu8Hc2TLgX4WhyzbZtgVUWoJJat6dcYMEUqoCBm_vDr9xrq7vYdz7WaltNkS_88xamsXdjNfdwcN5RrkVNu8zzfnxv97SUdxeJRuBDViqK4MxWUdBpOoLz83wJlYJ_wuq4kRZNo-iCN0m8PmTA_m5PnyxBdWGzuC1pROaZdpJ27SV9AUw81nhE6Ph9EAcGFVKteJ1BhM%3D)] It could animate:
    
    - Power flow changes along transmission lines (e.g., color changes, particle flows).[[14](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXGBrue9euig399W4I80TW_iZARKOkkjerEQHHCN7Ujh3lNIe25-aZJKsWedh0AAFoH-_VxvCm-TqfvuiM_Yqt5PMgXj6RDQdFJ6DrzyaIAfj2THzqWYVm6eeqqNuwzwKxHtDbm3hkuj553eGnT4bkOAUuSTFSLFYvsCN8eycIrSUQkgCSjfZA%3D%3D)][[15](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXECu8Hc2TLgX4WhyzbZtgVUWoJJat6dcYMEUqoCBm_vDr9xrq7vYdz7WaltNkS_88xamsXdjNfdwcN5RrkVNu8zzfnxv97SUdxeJRuBDViqK4MxWUdBpOoLz83wJlYJ_wuq4kRZNo-iCN0m8PmTA_m5PnyxBdWGzuC1pROaZdpJ27SV9AUw81nhE6Ph9EAcGFVKteJ1BhM%3D)]
        
    - The tripping of lines or failure of substations (e.g., lines disappearing, sparks).
        
    - The spread of the blackout across regions (e.g., areas darkening on the map).[[14](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXGBrue9euig399W4I80TW_iZARKOkkjerEQHHCN7Ujh3lNIe25-aZJKsWedh0AAFoH-_VxvCm-TqfvuiM_Yqt5PMgXj6RDQdFJ6DrzyaIAfj2THzqWYVm6eeqqNuwzwKxHtDbm3hkuj553eGnT4bkOAUuSTFSLFYvsCN8eycIrSUQkgCSjfZA%3D%3D)]
        
    - UI elements, like the timeline or information pop-ups.[[11](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXG9_V-UokpG4qM2ACbqiD3DM5550bAwyTdqviaqtUNI2S3LBOuSo1hWD91NuCv6ePGn2HDB8zvA9gt2yYNqGXUEgyGWME7xZOSywle0jkXuJUJ-zhUz2NfWQ4E5WXG0fKvN7pWLV_IwSFv7dNjzpV__G74-2QKx1DttdH_AU6c%3D)][[13](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXF5PrUVSd04seVyC9phsbTCBSHMtB9CkvEAZYPP2Tx_ODwa5ayPkZrTniQ1ip-BknKLhs3p97Ptit_CQvxhgr-uxBGh6B3_yL5HIltQnuFaxz3I1S7ICHq6Eb5mDuEMLsHWJInXlX3QeXoeRxegJqND)]
        

**I. Map Interface (Visualized with Three.js):**

- **Geographical Layout:** A 3D representation of Spain and Portugal.
    
- **Key Infrastructure:**
    
    - Major cities (dots or highlighted areas).
        
    - Power plants: Color-coded by type (e.g., solar PV, wind, hydro, nuclear, gas). Special emphasis on IBR locations.
        
    - Major substations (nodes in the grid).
        
    - High-voltage transmission lines interconnecting these elements.
        
- **Initial State:** The simulation would start with the grid fully operational, perhaps showing normal power flow animations.
    

**II. Timeline Feature:**

- **Interactive Control:** A draggable timeline slider or clickable time-step buttons representing the progression of the blackout event from T-0 (pre-disturbance) to T+10 hours (restoration phase).
    
- **Event Markers:** Key moments in the simulated blackout (e.g., initial trigger, first cascade, peak outage, start of restoration) would be marked on the timeline. Clicking these would jump the simulation to that point.
    

**III. Sidebar for Interactions, Scenarios & Information:**

- **Event Selection:**
    
    - The primary scenario would be the "Iberian Peninsula Blackout - April 28, 2025."
        
    - Potentially, users could select other generic triggers (e.g., "Large Generator Trip," "Major Transmission Line Fault," "Substation Failure at [Selectable Location]").
        
- **Cause Exploration (for the selected event):**
    
    - Dropdown or buttons to highlight the contributing factors as described:
        
        - "Show Inter-Area Oscillation Impact": Visualizes unstable power flows on tie-lines.
            
        - "Show High IBR Penetration Stress": Highlights areas with many IBRs and their response.
            
        - "Show Limited Interconnection Effect": Illustrates constraints on importing stabilizing power.
            
- **Layer Toggles:** Allow users to turn on/off map layers (e.g., IBR locations, population density, affected areas).
    
- **Information Display:** When an element (plant, line, region) is clicked or hovered over, this panel would display detailed information.
    

**IV. Visualizing Outages and Cascading Impact (Animated with Anime.js):**

- **Trigger Visualization:**
    
    - The simulation would visually depict the initial trigger: for the Iberian event, this would be the start of inter-area oscillations. Anime.js could show power flows on key lines becoming erratic or oscillating in color/intensity.[[16](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXGURXS-WbeXIJ-SzLZPk5TH650OPKH4RnyWtlXLVXhoEq_LLrnku6qaTnVkIZn2_OOKxSmtGiGeVNbG4TUq4cQe2mngkUHDGygl0JYXOnSQ3YV8wlUaGWb6TF7Jz4gOk70_-H9qYie0cGa58TOlk17Ocy9tf243Eq0wmNyPdtWbcZjrKM5u_fnQB8Fu-N0rlqNglzNm-ChpkmX-JCnN)][[17](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXGA_jeEkLC_ccsG8N3hAKTzK5zTY2BaRaUoFVqWKrcAfOoIGcbqP5N4UKnF4iuRwHvX7SQ8dxzF7SurfttsNPFASd-ptLKL-5RzDLJkqoa6Hb1KTqeJShlDNlasxol9R3_Id9xrBvuwI1ldn2_Nyd8ao1EiJsLwDzNu-AW5V8x_pBGRYpnbQysHtAphKg%3D%3D)][[18](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXE5np2oLjaQixt-R5-iI2GXXoEoCOEP9AIVl5xPMMVtVYkAWBM9rqL0Xo6Cv8y8M2aTvt-iRGwtrWWucRYMDbNcis9zHe58OcdNmzS2dXXRxgK-K2TMYbqrVtDxShdzxFZ6EOodA7YSIPCHKtmJ)][[19](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXHjlURwg3aTgI1Tw5V3POaHn5PGCVK_p6SooMakl-KnDMOCpwCJ6GIVc-ij8sNKKMyM2q-9DFLTU40nxakXRaxTbhIXU8kylCXOSFlHg4gcMNxkBgp6S49vVx6o1yqn1Q%3D%3D)][[20](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXHDSinYwzPcgGQ1qWVr5hCMK5j9V-cfjjs1eD_8g6jknGWrkW2MNKIJWrF3GrSGrmaitggJt-CZLULbXLNihvjwSnnzJeGZYYaK1JBf-EI4WD81UzXxJ2GBYFwCitXaiWB2KZ4e37MZrUH-Yybq6MDy3VHoLHIifML_Mu-mk7Ak7X5aUj1cli0sicaJjI_24vo-ChaZ3ns7ApOtnhTfSU1O46Yy8ezJ)]
        
- **Cascading Failures:**[[21](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXEjXsapt60qVQPAFDKRWcZOyLjlLNqpkNR2bEUN7xNF1A9KqsgCg9E6mBhXXLwFLjkCAL3EnRWAblO-Z1h4REqZMJFAst0pjXskVwj3j9qvsUSdBI5Ysc9S4sh5yLs1x0Uyun2t5g%3D%3D)][[22](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXHwQIduxMZsgZAgtp-tL9LihLjJM3sF9CdJH-7dzkGUhBqsI9Zxw-HjGH-_EODDF9qcjthcPhLRqhSnMPc3D99Ujileaq5C0AIgnPq4qlPivM_2Fky8RD3nRXX9f0rSCUyGcE33BTo9mABVQsb9CE1BShu1njrRhurxk6qWODdaXwv_AtphC8oDGCDfmByb_3Prwb2P1S7A26jx2aBl8Svb8O-XEDw77a1s8cb_)][[23](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXGlbqReBOciscJ3DmG_sxbB-JzmKymEwPZOlrBc8igIVN356juZCJSzsEN8YygRvw7uxhaEmbJiH9gQlxBgYqnf5f-83StnNyP5omLEHylZikFr7MrESp1KXhNmlPJFriyo58zX0jOFff1PItxJbw-MRkdQ9FBymzmyI1wB50dRCWLY5EoRBWYwiu8%3D)]
    
    - **Overloads:** As oscillations worsen or initial components trip, other lines would show increasing load (e.g., changing color from green to yellow to red).
        
    - **Tripping:** Lines exceeding their dynamic or thermal limits would "trip" – perhaps animated by disappearing, turning grey, or showing a spark animation.[[13](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXF5PrUVSd04seVyC9phsbTCBSHMtB9CkvEAZYPP2Tx_ODwa5ayPkZrTniQ1ip-BknKLhs3p97Ptit_CQvxhgr-uxBGh6B3_yL5HIltQnuFaxz3I1S7ICHq6Eb5mDuEMLsHWJInXlX3QeXoeRxegJqND)]
        
    - **IBR Response:** Areas with high IBR might show many units tripping offline simultaneously (flickering off), visually demonstrating the impact of their protection settings or lack of grid-forming capabilities in this scenario.[[24](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXFTRPS0UCZdUbx1pQRw4uOL55gCEUgt6KOxwAeoqZG41togLh8yhzP2L_849Y3f-vF6yHj0JO-Z0A63bj8IVphIOIY3IAh4-2IubDU2onOsei7KguUdK2UOurcWy6gi)][[25](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXHD_sMCpdNjLCjkBCdaP3JSLyJp71LJmWEKhYEE7wJcHO5ZPG0VMwkPzzVhXuF8kx94ATReV4Q0NMh-9h5jKOGcyWxETz5CElZVxfyc4POJLW0erRunTRinEYjkeZoNstuXhyF90zRpHRIFqQ%3D%3D)][[26](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXEB-BSTpMRPyjo9qz0y64xpSzTxJyWh92oC9CLqVAycWWi0brHmdSz_SpNkK8Ugd-zfpgcxNnfcxTqybDeLQEqgaRJrXsN-9ZCfN5SsTe7vUO7j0zct029siRUBWy2gFsBcwIsdURUsopJaGv4oVQWOsx4VOTh-D0theyTQj4Ns2efWaGazb3QjMLhjT8lMSBOZfInXsuQl-Av1qWyefuY_3wmd3O8jocb49M_WZ3_Vy79UAApQyTs95lcg92Ne3hK4o1akZrUGHZQKPdtGo3k6Ag%3D%3D)][[27](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXGJcFMWdWUGVGvS70GH4X6MHo9-Nlj0pf_Q1SNg3fO16fMkTQx1UWJcQ_i-X2OL24PAjcaK6VePr_zUb24X_BBOzGyqy9icksk87U61j7LP-90rhFkSY5lbot9aIiUn7YbN29oWg5SFOucMmReazKSzeCAsDe_vZnnPI5hMDC3bRA%3D%3D)][[28](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXGJp_cyeiFkEHWjTCIgK34B8mrKh45MV_RpZlgE9go3ARGDHeQVFZXJBx6KRQUwlBe03J_H9nrjtox_fay427-B6xUlczGF9hCnuZF0xVpKyOPk3sP2hFbgo5nY8ABuYwBC2MdnkbaYdyDvgCHDzcSHKS9eB2hS3MpdgD-wOYXn8fBAqisv9qwhwqQb-Ql93OxdmFi11DpD2BJIXj9HheoxZE9sO8DjI0Di9xpIniGOftGzaA%3D%3D)]
        
    - **Outage Spread:** Regions losing power would darken on the map, with the blackout area expanding dynamically based on the simulated cascade.
        
    - **System Separation:** If parts of the grid become isolated, this could be shown by distinct, non-synchronized areas.
        
- **Dynamic Interactions (on click/hover):**
    
    - **Power Plants:** Display type (IBR, synchronous), capacity, real-time (simulated) output, status (online/offline/tripped).
        
    - **Transmission Lines:** Show (simulated) power flow, capacity, status, and stress level.
        
    - **Substations:** Indicate connectivity, load, and operational status.
        
    - **Regions/Cities:** Display population, estimated demand, and power status (powered/blacked out/partially powered). Anime.js could animate these info panels appearing smoothly.[[11](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXG9_V-UokpG4qM2ACbqiD3DM5550bAwyTdqviaqtUNI2S3LBOuSo1hWD91NuCv6ePGn2HDB8zvA9gt2yYNqGXUEgyGWME7xZOSywle0jkXuJUJ-zhUz2NfWQ4E5WXG0fKvN7pWLV_IwSFv7dNjzpV__G74-2QKx1DttdH_AU6c%3D)][[14](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXGBrue9euig399W4I80TW_iZARKOkkjerEQHHCN7Ujh3lNIe25-aZJKsWedh0AAFoH-_VxvCm-TqfvuiM_Yqt5PMgXj6RDQdFJ6DrzyaIAfj2THzqWYVm6eeqqNuwzwKxHtDbm3hkuj553eGnT4bkOAUuSTFSLFYvsCN8eycIrSUQkgCSjfZA%3D%3D)]
        

**V. Math and Energy Science Integration (Conceptual Backend):**

The simulation's behavior would be driven by simplified models based on established energy science principles, as detailed in the provided texts:

- **Power Flow:**
    
    - Simplified AC or DC power flow calculations to determine how power is redistributed after a component fails. The user's text mentions Fij(t) = Kij sin(θi(t) - θj(t)) from the swing equation context.
        
- **Dynamic Stability & Oscillations:**
    
    - The concept of inter-area oscillations (typically 0.1-1.5 Hz) being triggered and potentially growing due to system conditions.[[16](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXGURXS-WbeXIJ-SzLZPk5TH650OPKH4RnyWtlXLVXhoEq_LLrnku6qaTnVkIZn2_OOKxSmtGiGeVNbG4TUq4cQe2mngkUHDGygl0JYXOnSQ3YV8wlUaGWb6TF7Jz4gOk70_-H9qYie0cGa58TOlk17Ocy9tf243Eq0wmNyPdtWbcZjrKM5u_fnQB8Fu-N0rlqNglzNm-ChpkmX-JCnN)][[17](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXGA_jeEkLC_ccsG8N3hAKTzK5zTY2BaRaUoFVqWKrcAfOoIGcbqP5N4UKnF4iuRwHvX7SQ8dxzF7SurfttsNPFASd-ptLKL-5RzDLJkqoa6Hb1KTqeJShlDNlasxol9R3_Id9xrBvuwI1ldn2_Nyd8ao1EiJsLwDzNu-AW5V8x_pBGRYpnbQysHtAphKg%3D%3D)][[18](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXE5np2oLjaQixt-R5-iI2GXXoEoCOEP9AIVl5xPMMVtVYkAWBM9rqL0Xo6Cv8y8M2aTvt-iRGwtrWWucRYMDbNcis9zHe58OcdNmzS2dXXRxgK-K2TMYbqrVtDxShdzxFZ6EOodA7YSIPCHKtmJ)][[19](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXHjlURwg3aTgI1Tw5V3POaHn5PGCVK_p6SooMakl-KnDMOCpwCJ6GIVc-ij8sNKKMyM2q-9DFLTU40nxakXRaxTbhIXU8kylCXOSFlHg4gcMNxkBgp6S49vVx6o1yqn1Q%3D%3D)] The simulation wouldn't necessarily solve complex differential equations in real-time in a browser, but it would model their effects based on predefined parameters related to the scenario.
        
    - The swing equation principles (Ii d²θi/dt² + γi dθi/dt = Pi - Σj Kij sin(θi - θj)) describe the electromechanical dynamics. The simulation could reflect how reduced inertia (common with high IBR) leads to faster frequency deviations.[[26](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXEB-BSTpMRPyjo9qz0y64xpSzTxJyWh92oC9CLqVAycWWi0brHmdSz_SpNkK8Ugd-zfpgcxNnfcxTqybDeLQEqgaRJrXsN-9ZCfN5SsTe7vUO7j0zct029siRUBWy2gFsBcwIsdURUsopJaGv4oVQWOsx4VOTh-D0theyTQj4Ns2efWaGazb3QjMLhjT8lMSBOZfInXsuQl-Av1qWyefuY_3wmd3O8jocb49M_WZ3_Vy79UAApQyTs95lcg92Ne3hK4o1akZrUGHZQKPdtGo3k6Ag%3D%3D)]
        
- **IBR Behavior:**[[24](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXFTRPS0UCZdUbx1pQRw4uOL55gCEUgt6KOxwAeoqZG41togLh8yhzP2L_849Y3f-vF6yHj0JO-Z0A63bj8IVphIOIY3IAh4-2IubDU2onOsei7KguUdK2UOurcWy6gi)][[25](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXHD_sMCpdNjLCjkBCdaP3JSLyJp71LJmWEKhYEE7wJcHO5ZPG0VMwkPzzVhXuF8kx94ATReV4Q0NMh-9h5jKOGcyWxETz5CElZVxfyc4POJLW0erRunTRinEYjkeZoNstuXhyF90zRpHRIFqQ%3D%3D)][[26](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXEB-BSTpMRPyjo9qz0y64xpSzTxJyWh92oC9CLqVAycWWi0brHmdSz_SpNkK8Ugd-zfpgcxNnfcxTqybDeLQEqgaRJrXsN-9ZCfN5SsTe7vUO7j0zct029siRUBWy2gFsBcwIsdURUsopJaGv4oVQWOsx4VOTh-D0theyTQj4Ns2efWaGazb3QjMLhjT8lMSBOZfInXsuQl-Av1qWyefuY_3wmd3O8jocb49M_WZ3_Vy79UAApQyTs95lcg92Ne3hK4o1akZrUGHZQKPdtGo3k6Ag%3D%3D)][[27](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXGJcFMWdWUGVGvS70GH4X6MHo9-Nlj0pf_Q1SNg3fO16fMkTQx1UWJcQ_i-X2OL24PAjcaK6VePr_zUb24X_BBOzGyqy9icksk87U61j7LP-90rhFkSY5lbot9aIiUn7YbN29oWg5SFOucMmReazKSzeCAsDe_vZnnPI5hMDC3bRA%3D%3D)][[28](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXGJp_cyeiFkEHWjTCIgK34B8mrKh45MV_RpZlgE9go3ARGDHeQVFZXJBx6KRQUwlBe03J_H9nrjtox_fay427-B6xUlczGF9hCnuZF0xVpKyOPk3sP2hFbgo5nY8ABuYwBC2MdnkbaYdyDvgCHDzcSHKS9eB2hS3MpdgD-wOYXn8fBAqisv9qwhwqQb-Ql93OxdmFi11DpD2BJIXj9HheoxZE9sO8DjI0Di9xpIniGOftGzaA%3D%3D)]
    
    - **High IBR Penetration:** The simulation would visually represent the large percentage of IBRs.
        
    - **IBR Response to Disturbances:** Model how grid-following IBRs might trip or reduce output during frequency/voltage events if they lack advanced grid-forming capabilities. The scenario notes "limited dynamic support."
        
    - **Grid-Forming vs. Grid-Following:** Conceptually, the sidebar could allow toggling the percentage of "advanced IBRs (grid-forming)" to see if the blackout's severity changes.
        
- **Line & Component Limits:**
    
    - Lines would have defined capacities (Cij = αKij). If flow Fij exceeds Cij, the line trips. This is a core part of cascading failure models.[[21](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXEjXsapt60qVQPAFDKRWcZOyLjlLNqpkNR2bEUN7xNF1A9KqsgCg9E6mBhXXLwFLjkCAL3EnRWAblO-Z1h4REqZMJFAst0pjXskVwj3j9qvsUSdBI5Ysc9S4sh5yLs1x0Uyun2t5g%3D%3D)][[22](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXHwQIduxMZsgZAgtp-tL9LihLjJM3sF9CdJH-7dzkGUhBqsI9Zxw-HjGH-_EODDF9qcjthcPhLRqhSnMPc3D99Ujileaq5C0AIgnPq4qlPivM_2Fky8RD3nRXX9f0rSCUyGcE33BTo9mABVQsb9CE1BShu1njrRhurxk6qWODdaXwv_AtphC8oDGCDfmByb_3Prwb2P1S7A26jx2aBl8Svb8O-XEDw77a1s8cb_)]
        
- **Interconnection Capacity:**[[29](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXFZ5NNVPxaGldIbqTWws9E4TRTi62GyZHoRpdeHd_et0MD5Kov4PgYCf5dQ3lL5mLiu8THAiGcrsNEV7tg6U5QVCpjHspV9PadRQk4L1xYoqXDmYNxZO3NKSE9nDg-MevKa6RON2szclLhYHml3wWiV_axSHNnaQ0EnGm5vnmDKPO2qiFatr8pD_H9Z2WEnbtPD54FZir0I1N2uUD_q3u8K1d5QJCuwdsKsewKOa9H4ow%3D%3D)][[30](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXGeR9-MHZmQSlDxQdsSf48YRNhZvVPtY0RNaeBkZMpxJCXXI4yBOSWdJPuWYortyDr4FjRRfTqu-utM1HzMIPweTCFqE8nhAwCAevhH_cL-8m-O2hvPgULimwUIcJxaoPHVroZxgT5QmwgvLPUASdcRpQo-Xu9GuM2YIsGVsyLldlKeiTYPUufLKBsHpWdRJa0%3D)][[31](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXFUnSD4XZcfg8E8pDhVQ_kYp0H4BSpyHlOk68EfHxqKgDUxLRrke8eI64Os1wOxR9_3fYzp9bn5TqLX3HnST0rXxXlJkSYWDkBd4SDQZyAXxXPhIsh8xVHNOuo-IbwEuWs7eyZshkq5TLmJj2n1ktVhYzPub6tMR9QMbMdEcXPXsfeoE23wY8TaVN3o8rkMiJe0Uu4%3D)][[32](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXExnR_oiBqZ_nfGvcvAgr63UyQeajUGtDEwTLJG98TKOuhZ0fqve7IT-E-IKMlfUZn-tmgi9-5YWQbWdYZ4HgM54626DyV8CrdJ0aPnnz5dkpfSC2pp_xAw7HXpBaawJUTuJx9_RFk8BUaVTXXlueNzuzHz847JuS1yPlsSO3YmMWZO0HSt_t-280fgIaisYQocNRnm)][[33](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXGmlMHUeCFDkbKervh7cw15gqAUjCtZuffgQl-EhweUgHIeDaPYTxz9Bh4LM_gNHq4ki-f7A2IE_q_rnn3jXL4xnpytvajnjAclV6XFhKe27wCGCWsBlfegpE5aIpIuavNOFYR06RCVQ7Mc8mgCBldNPWytnQ0qvibxit7QK9Q5cen_j-N7kLB64QY9QHcxlXBCLZxvqqXiJJZ14I_aZ-_TdTHiIArxxR-Q5NmqTzE6BNhg2SH8xWKrH1ZYCSeYWQHEJxTI2wCHqz0Z9QCI)]
    
    - The simulation would represent the limited interconnection capacity between the Iberian Peninsula and the rest of Europe. During the simulated event, this limit would restrict the import of power that could help stabilize the system.
        
- **N-1 (and beyond) Criteria:**
    
    - The simulation would demonstrate how an initial event (N-1, or N-2 as per some models[[34](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXFRb2NCv-wtJ4nxhLs-vIa1hbfH4RHApkmbyxijWpVb71mOcnKi-MGEnIDFZoD1oEXkzH6JVNGKv62xpeOeBG6KeN-tsUt3EM0QyA8VUhKhioCOWFsMn6PRF9D9mj_S5gLuybHz2DrWH_iCyRqdSXnGPiwGNesi3MspGfTHTh1zvG7pDrSD0D-aejSHSDO4LxwCTMDECvdcUfIkWVuuzgilR0wL_Dt2OxUy2SF8FZkZHOToHWexfaD2C4tpyQXn7TOykOJhSO9Oh6rRzVG6n8tyeoa5)]) could lead to a cascade far exceeding simple static N-1 security assessments, especially due to dynamic phenomena.[[22](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXHwQIduxMZsgZAgtp-tL9LihLjJM3sF9CdJH-7dzkGUhBqsI9Zxw-HjGH-_EODDF9qcjthcPhLRqhSnMPc3D99Ujileaq5C0AIgnPq4qlPivM_2Fky8RD3nRXX9f0rSCUyGcE33BTo9mABVQsb9CE1BShu1njrRhurxk6qWODdaXwv_AtphC8oDGCDfmByb_3Prwb2P1S7A26jx2aBl8Svb8O-XEDw77a1s8cb_)][[34](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXFRb2NCv-wtJ4nxhLs-vIa1hbfH4RHApkmbyxijWpVb71mOcnKi-MGEnIDFZoD1oEXkzH6JVNGKv62xpeOeBG6KeN-tsUt3EM0QyA8VUhKhioCOWFsMn6PRF9D9mj_S5gLuybHz2DrWH_iCyRqdSXnGPiwGNesi3MspGfTHTh1zvG7pDrSD0D-aejSHSDO4LxwCTMDECvdcUfIkWVuuzgilR0wL_Dt2OxUy2SF8FZkZHOToHWexfaD2C4tpyQXn7TOykOJhSO9Oh6rRzVG6n8tyeoa5)]
        

**VI. Simulated Timeline of the Iberian Peninsula Blackout (April 28, 2025):**

This timeline would be animated on the map and controllable via the timeline feature:

- **T-0 (Pre-Disturbance State - e.g., 12:00 PM):**
    
    - **Map:** Shows normal operation. High IBR (solar, wind) feeding the grid across Spain and Portugal. Power flows are stable.
        
    - **Data:** System frequency nominal (50Hz). Interconnection flows are within limits.
        
- **T+0 to T+2 Minutes (Initial Disturbance - e.g., 12:30 PM - 12:32 PM):**
    
    - **Cause:** Suspected inter-area oscillations begin, perhaps triggered by a minor remote event or inherent system instability under current conditions.[[16](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXGURXS-WbeXIJ-SzLZPk5TH650OPKH4RnyWtlXLVXhoEq_LLrnku6qaTnVkIZn2_OOKxSmtGiGeVNbG4TUq4cQe2mngkUHDGygl0JYXOnSQ3YV8wlUaGWb6TF7Jz4gOk70_-H9qYie0cGa58TOlk17Ocy9tf243Eq0wmNyPdtWbcZjrKM5u_fnQB8Fu-N0rlqNglzNm-ChpkmX-JCnN)][[17](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXGA_jeEkLC_ccsG8N3hAKTzK5zTY2BaRaUoFVqWKrcAfOoIGcbqP5N4UKnF4iuRwHvX7SQ8dxzF7SurfttsNPFASd-ptLKL-5RzDLJkqoa6Hb1KTqeJShlDNlasxol9R3_Id9xrBvuwI1ldn2_Nyd8ao1EiJsLwDzNu-AW5V8x_pBGRYpnbQysHtAphKg%3D%3D)]
        
    - **Map Animation (Anime.js):** Key inter-regional or international tie-lines start showing oscillating power flows (e.g., flickering, color cycling rapidly).
        
    - **Sidebar Info:** Highlights "Inter-area oscillations detected."
        
- **T+2 to T+5 Minutes (Escalation - e.g., 12:32 PM - 12:35 PM):**
    
    - **Description:** Oscillations amplify. High IBR penetration with predominantly grid-following inverters contributes to faster frequency deviations and provides limited damping or inertial response.[[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXFlZvv7erN1VDhPSgs_RPI2L1b_SihhMC17YRjTV5s9GJXkpYQuoTeUi-dFAHOGW7ny_sGEhrQgACJGe0531_SngmO2Gv_G93viTQIzZABw3l1U8YA7SMBXwrVZm84yYEM-v59O_s5hEhOq9I-MeELpahZjvjgaC25IfsfaG0rjbB9Ixhku0hn3fidNiv0%3D)][[24](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXFTRPS0UCZdUbx1pQRw4uOL55gCEUgt6KOxwAeoqZG41togLh8yhzP2L_849Y3f-vF6yHj0JO-Z0A63bj8IVphIOIY3IAh4-2IubDU2onOsei7KguUdK2UOurcWy6gi)][[26](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXEB-BSTpMRPyjo9qz0y64xpSzTxJyWh92oC9CLqVAycWWi0brHmdSz_SpNkK8Ugd-zfpgcxNnfcxTqybDeLQEqgaRJrXsN-9ZCfN5SsTe7vUO7j0zct029siRUBWy2gFsBcwIsdURUsopJaGv4oVQWOsx4VOTh-D0theyTQj4Ns2efWaGazb3QjMLhjT8lMSBOZfInXsuQl-Av1qWyefuY_3wmd3O8jocb49M_WZ3_Vy79UAApQyTs95lcg92Ne3hK4o1akZrUGHZQKPdtGo3k6Ag%3D%3D)][[28](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXGJp_cyeiFkEHWjTCIgK34B8mrKh45MV_RpZlgE9go3ARGDHeQVFZXJBx6KRQUwlBe03J_H9nrjtox_fay427-B6xUlczGF9hCnuZF0xVpKyOPk3sP2hFbgo5nY8ABuYwBC2MdnkbaYdyDvgCHDzcSHKS9eB2hS3MpdgD-wOYXn8fBAqisv9qwhwqQb-Ql93OxdmFi11DpD2BJIXj9HheoxZE9sO8DjI0Di9xpIniGOftGzaA%3D%3D)] Some IBRs may start tripping due to voltage/frequency protection.
        
    - **Map Animation:** More lines show stress. Some IBR plant icons start to dim or turn red/offline. System frequency (displayed) starts to fluctuate more visibly.
        
- **T+5 to T+15 Minutes (First Cascades - e.g., 12:35 PM - 12:45 PM):**
    
    - **Description:** Critical transmission lines overload due to the erratic flows and loss of generation, then trip.[[21](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXEjXsapt60qVQPAFDKRWcZOyLjlLNqpkNR2bEUN7xNF1A9KqsgCg9E6mBhXXLwFLjkCAL3EnRWAblO-Z1h4REqZMJFAst0pjXskVwj3j9qvsUSdBI5Ysc9S4sh5yLs1x0Uyun2t5g%3D%3D)] This could be on major corridors within Spain/Portugal or on the interconnectors with France. The limited interconnection capacity to the wider European grid becomes a critical factor, unable to provide sufficient support.[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXEymwZlB2dPi4LwkKyNF6PAfbUiGgM6J1KgFvI4m4rhF72z3PDpw3s9ZBRnXWnZVEtzsHbBLSqcoarvvDlEP9qwunbc2GF97Irza3IeZpEg0Vd45SzTi0SUoVsXoVR8gGAVG1xZSLxKDFT8JEUPt72NZ5IG1E-4-kD5ewITeNavOXLryIvIyX2Gq2efrIGL22HrqMno4XyIXBLi2ftEStVtfY4%3D)][[29](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXFZ5NNVPxaGldIbqTWws9E4TRTi62GyZHoRpdeHd_et0MD5Kov4PgYCf5dQ3lL5mLiu8THAiGcrsNEV7tg6U5QVCpjHspV9PadRQk4L1xYoqXDmYNxZO3NKSE9nDg-MevKa6RON2szclLhYHml3wWiV_axSHNnaQ0EnGm5vnmDKPO2qiFatr8pD_H9Z2WEnbtPD54FZir0I1N2uUD_q3u8K1d5QJCuwdsKsewKOa9H4ow%3D%3D)]
        
    - **Map Animation:** Lines turn red and then disappear. Small areas around these tripped lines start to go dark. Alarms could flash at affected substations.
        
- **T+15 Minutes to T+1 Hour (Widespread Cascading Failure - e.g., 12:45 PM - 1:30 PM):**
    
    - **Description:** The initial outages lead to a domino effect. Large sections of the grid become unstable, leading to further tripping of lines and generators to protect equipment. Significant portions of Spain and Portugal experience blackouts.[[21](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXEjXsapt60qVQPAFDKRWcZOyLjlLNqpkNR2bEUN7xNF1A9KqsgCg9E6mBhXXLwFLjkCAL3EnRWAblO-Z1h4REqZMJFAst0pjXskVwj3j9qvsUSdBI5Ysc9S4sh5yLs1x0Uyun2t5g%3D%3D)][[22](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXHwQIduxMZsgZAgtp-tL9LihLjJM3sF9CdJH-7dzkGUhBqsI9Zxw-HjGH-_EODDF9qcjthcPhLRqhSnMPc3D99Ujileaq5C0AIgnPq4qlPivM_2Fky8RD3nRXX9f0rSCUyGcE33BTo9mABVQsb9CE1BShu1njrRhurxk6qWODdaXwv_AtphC8oDGCDfmByb_3Prwb2P1S7A26jx2aBl8Svb8O-XEDw77a1s8cb_)] The system may split into unmanageable islands.
        
    - **Map Animation:** Large swathes of Spain and Portugal darken progressively. The "People Affected" counter in the sidebar rapidly increases towards 60 million.
        
- **T+1 Hour to T+10 Hours (Peak Outage & Initial Restoration - e.g., 1:30 PM onwards):**
    
    - **Description:** The blackout reaches its maximum extent. Millions are without power. Grid operators begin the slow and complex process of system diagnosis, stabilizing isolated sections, and carefully restoring power (black start).[[4](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXHASmlWvzWMytAs3ZPsn-n8jWN20Hs7bevplAhNNo_iCP9cXYxLC-ejB-OM2PxwCjnt2Oq6NnDbTZhATkPPTf0mFWOi58f0kQ_fUklXe0D75e-hv8V_rF9WhiulQQI3e4gwIDjXaPI-F78amyzX8JA-ebLdti4ZOQyPWixMMjELYhHE2ezEeABdrIagG-SLKvR_PdawE86zu_eyOMLX)] Challenges include managing IBRs during restoration.
        
    - **Map Animation:** Most of the peninsula is dark. After some time (e.g., T+3 hours), small areas might begin to light up again very slowly and sequentially, indicating restoration efforts.
        
    - **Sidebar Info:** Shows duration of outage, updates on restoration progress.
        

**VII. Key Learnings (Interactive Exploration):**

The sidebar could have a "Key Learnings" section. Clicking on each point could re-run parts of the simulation or highlight aspects on the map:

- **"Grid Stability with High IBR":** Highlight areas with high IBR. Show statistics on their contribution pre-blackout and their behavior during the event. Perhaps offer a "what-if" scenario where more IBRs have grid-forming capabilities, showing a less severe outage.[[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXFlZvv7erN1VDhPSgs_RPI2L1b_SihhMC17YRjTV5s9GJXkpYQuoTeUi-dFAHOGW7ny_sGEhrQgACJGe0531_SngmO2Gv_G93viTQIzZABw3l1U8YA7SMBXwrVZm84yYEM-v59O_s5hEhOq9I-MeELpahZjvjgaC25IfsfaG0rjbB9Ixhku0hn3fidNiv0%3D)][[24](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXFTRPS0UCZdUbx1pQRw4uOL55gCEUgt6KOxwAeoqZG41togLh8yhzP2L_849Y3f-vF6yHj0JO-Z0A63bj8IVphIOIY3IAh4-2IubDU2onOsei7KguUdK2UOurcWy6gi)][[26](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXEB-BSTpMRPyjo9qz0y64xpSzTxJyWh92oC9CLqVAycWWi0brHmdSz_SpNkK8Ugd-zfpgcxNnfcxTqybDeLQEqgaRJrXsN-9ZCfN5SsTe7vUO7j0zct029siRUBWy2gFsBcwIsdURUsopJaGv4oVQWOsx4VOTh-D0theyTQj4Ns2efWaGazb3QjMLhjT8lMSBOZfInXsuQl-Av1qWyefuY_3wmd3O8jocb49M_WZ3_Vy79UAApQyTs95lcg92Ne3hK4o1akZrUGHZQKPdtGo3k6Ag%3D%3D)][[28](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXGJp_cyeiFkEHWjTCIgK34B8mrKh45MV_RpZlgE9go3ARGDHeQVFZXJBx6KRQUwlBe03J_H9nrjtox_fay427-B6xUlczGF9hCnuZF0xVpKyOPk3sP2hFbgo5nY8ABuYwBC2MdnkbaYdyDvgCHDzcSHKS9eB2hS3MpdgD-wOYXn8fBAqisv9qwhwqQb-Ql93OxdmFi11DpD2BJIXj9HheoxZE9sO8DjI0Di9xpIniGOftGzaA%3D%3D)]
    
- **"Interconnection Capacity":** Emphasize the limited flow on interconnectors. A "what-if" scenario with increased interconnection capacity could show more support power flowing in, potentially mitigating the cascade.[[29](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXFZ5NNVPxaGldIbqTWws9E4TRTi62GyZHoRpdeHd_et0MD5Kov4PgYCf5dQ3lL5mLiu8THAiGcrsNEV7tg6U5QVCpjHspV9PadRQk4L1xYoqXDmYNxZO3NKSE9nDg-MevKa6RON2szclLhYHml3wWiV_axSHNnaQ0EnGm5vnmDKPO2qiFatr8pD_H9Z2WEnbtPD54FZir0I1N2uUD_q3u8K1d5QJCuwdsKsewKOa9H4ow%3D%3D)][[30](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXGeR9-MHZmQSlDxQdsSf48YRNhZvVPtY0RNaeBkZMpxJCXXI4yBOSWdJPuWYortyDr4FjRRfTqu-utM1HzMIPweTCFqE8nhAwCAevhH_cL-8m-O2hvPgULimwUIcJxaoPHVroZxgT5QmwgvLPUASdcRpQo-Xu9GuM2YIsGVsyLldlKeiTYPUufLKBsHpWdRJa0%3D)][[31](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXFUnSD4XZcfg8E8pDhVQ_kYp0H4BSpyHlOk68EfHxqKgDUxLRrke8eI64Os1wOxR9_3fYzp9bn5TqLX3HnST0rXxXlJkSYWDkBd4SDQZyAXxXPhIsh8xVHNOuo-IbwEuWs7eyZshkq5TLmJj2n1ktVhYzPub6tMR9QMbMdEcXPXsfeoE23wY8TaVN3o8rkMiJe0Uu4%3D)][[32](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXExnR_oiBqZ_nfGvcvAgr63UyQeajUGtDEwTLJG98TKOuhZ0fqve7IT-E-IKMlfUZn-tmgi9-5YWQbWdYZ4HgM54626DyV8CrdJ0aPnnz5dkpfSC2pp_xAw7HXpBaawJUTuJx9_RFk8BUaVTXXlueNzuzHz847JuS1yPlsSO3YmMWZO0HSt_t-280fgIaisYQocNRnm)]
    
- **"Advanced IBR Control (Grid-Forming)":** Clicking this could show a conceptual animation of how grid-forming inverters would respond differently (e.g., providing inertial response, actively supporting voltage/frequency) compared to the baseline grid-following scenario.[[25](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXHD_sMCpdNjLCjkBCdaP3JSLyJp71LJmWEKhYEE7wJcHO5ZPG0VMwkPzzVhXuF8kx94ATReV4Q0NMh-9h5jKOGcyWxETz5CElZVxfyc4POJLW0erRunTRinEYjkeZoNstuXhyF90zRpHRIFqQ%3D%3D)][[28](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAbF9wXGJp_cyeiFkEHWjTCIgK34B8mrKh45MV_RpZlgE9go3ARGDHeQVFZXJBx6KRQUwlBe03J_H9nrjtox_fay427-B6xUlczGF9hCnuZF0xVpKyOPk3sP2hFbgo5nY8ABuYwBC2MdnkbaYdyDvgCHDzcSHKS9eB2hS3MpdgD-wOYXn8fBAqisv9qwhwqQb-Ql93OxdmFi11DpD2BJIXj9HheoxZE9sO8DjI0Di9xpIniGOftGzaA%3D%3D)]
    

**VIII. IBR Impact Visualization (Very High):**

- A dedicated view or layer that shows:
    
    - Percentage of generation from IBRs before the event.
        
    - Animated sequence of IBRs tripping offline or reducing output significantly as instability grows.
        
    - Graphs showing the rapid loss of IBR generation compared to the slower response or trip of conventional plants.
        

By combining these elements, your simulation could provide a powerful visual and interactive narrative of the complex dynamics leading to and evolving from a major power grid blackout, grounded in real-world energy science concepts and the specifics of your hypothetical event.

Sources