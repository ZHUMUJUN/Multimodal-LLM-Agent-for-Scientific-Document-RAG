# 11_anthropogenic_photons_light_pollution_arxiv

## Page 1

1 
 
 
Light pollution and the concentration of anthropogenic 
photons in the terrestrial atmosphere 
 
 
Salvador Bará1,*, Carmen Bao-Varela2, and Fabio Falchi2,3 
1 A. Astronómica 'Ío', 15005 A Coruña, Galicia (Spain) 
2 Photonics4Life Research Group, Applied Physics Department, Universidade de 
Santiago de Compostela, Campus Vida, E-15782 Santiago de Compostela, Spain 
3 Istituto di Scienza e Tecnologia dell’Inquinamento Luminoso (ISTIL), 36016 Thiene, 
Italy 
 
(*) Corresponding author. email: salva.bara@usc.gal  
ORCID SB: https://orcid.org/0000-0003-1274-8043 
ORCID CB-V: https://orcid.org/0000-0002-0602-800X 
ORCID FF: https://orcid.org/0000-0002-3706-5639 
 
Abstract 
Light pollution can be rigorously described in terms of the volume concentration of 
anthropogenic photons (light quanta) in the terrestrial atmosphere. This formulation, 
consistent with the basic physics of the emission, scattering and absorption of light, 
allows one to express light pollution levels in terms of particle volume concentrations, 
in a completely analogous way as it is currently done with other classical pollutants, like 
particulate matter or molecular contaminants. In this work we provide the explicit 
conversion equations between the photon volume concentration and the traditional 
light photometry quantities. This equivalent description of the light pollution levels 
provides some relevant insights that help to identify artificial light at night as a standard 
pollutant. It also enables a complementary way of expressing artificial light exposures 
for environmental and public health research and regulatory purposes. 
 
Keywords 
Light pollution ; nocturnal environment ; radiometry ; photometry ; air pollution  
 
 
CC-BY-NC-ND This is an author-formatted version of the accepted manuscript whose version of 
record has been published in Atmospheric Pollution Research, 2022, 13(9):101541, 
https://doi.org/10.1016/j.apr.2022.101541

## Page 2

2 
 
 
1. Introduction 
Artificial light at night is a key factor for the improvement of the living conditions of 
humankind. Its production and control have provided us an essential level of freedom, 
enabling many activities at nighttime that otherwise would be limited by the low 
performance of the human visual system under typical natural night light levels. Artificial 
light at night is also a longtime recognized air pollutant. Already in 1979, the UN 
Convention on Long-range Transboundary Air Pollution, in its art. 1.a), established that 
“"Air Pollution" means the introduction by man, directly or indirectly, of substances 
or energy into the air resulting in deleterious effects of such a nature as to endanger 
human health, harm living resources and ecosystems and material property and 
impair or interfere with amenities and other legitimate uses of the environment, 
and "air pollutants" shall be construed accordingly" (United Nations, 1996) 
with an explicit and consistent interpretation by the UN International Law Commission 
in the sense that, in the context of the protection of the atmosphere, 
““Energy” is understood to include heat, light, noise and radioactivity introduced 
and released into the atmosphere through human activities” (United Nations, 
2018). 
 
Artificial light at night has been shown to produce undesired disruptive effects on 
wildlife (Longcore and Rich, 2004; Rich and Longcore, 2006; Hölker et al., 2010; Davies 
et al., 2013; Svechkina et al., 2020; Gaston et al., 2021) as well as in relevant aspects of 
human health (Davis et al., 2001; Haim and Portnov, 2013; Stevens et al., 2014; 
Smolensky et al., 2015; García-Sáenz et al., 2018; Russart and Nelson, 2018; Boyce, 
2022). These unwanted effects add to the progressive loss of the starry night sky 
(Cinzano et al., 2001; Falchi et al., 2016; Bará, 2016), whose negative consequences for 
the sustainability of the scientific activity of ground-based astronomical observatories 
(Walker, 1970; Garstang, 1989; Green et al., 2022), and the preservation of humankind's 
intangible cultural heritage (Marin and Jafari, 2008) have been noticed since longtime 
ago. Light pollution levels increase at a steady rate worldwide (Kyba et al., 2017), and 
their overall impact on the nocturnal environment is an issue of concern, as expressed 
in a growing body of recommendations (see, e.g., International Astronomical Union, 
1976; Americal Medical Association, 2012; European Union, 2018; IARC, 2019; 
Convention on Migratory Species, 2020; International Union for Conservation of Nature, 
2021; Brown et al., 2022).   
 
Being inextricably linked to human visual experience, light has been traditionally 
measured and described using specific visual photometric quantities based on the 
candela (𝑐𝑑), one of the seven basic units of the international system, SI (BIPM, 2018). 
Visual photometric quantities are related to their physical radiometric counterparts 
through an internationally agreed set of well-defined conversions, mostly based on the

## Page 3

3 
 
CIE 𝑉𝜆 function, the photopic spectral sensitivity of the human visual system (CIE, 1926). 
By applying these conversions, the spectral radiance of the electromagnetic field 
(usually given in energy units 𝑊· 𝑚−2 · 𝑠𝑟−1 · 𝑛𝑚−1) can be straightforwardly 
transformed to visual luminance (𝑐𝑑· 𝑚−2).   
 
The quantum nature of light is an essential feature of our universe, and the 
emission, scattering and absorption processes of light are often more adequately 
described in terms of discrete light quanta (photons) than in terms of continuous 
distributions of energy (Einstein, 1905). The discrete formulation is particularly well 
suited for environmental studies where light plays an essential role as the basic visual 
input (Nilsson and Smolka, 2021; Nilsson et al, 2022), since the photochemical 
interactions in the eye retina take place on a photon by photon basis, and also in those 
cases where very low illumination levels reveal the granular nature of light. Accordingly, 
the spectral radiance is also commonly specified using discrete photon numbers 
(𝑝ℎ𝑜𝑡𝑜𝑛𝑠· 𝑠−1 · 𝑚−2 · 𝑠𝑟−1 · 𝑛𝑚−1) 
based 
on 
the 
photon 
energy 
𝑄𝑝ℎ𝑜𝑡=
ℎ𝜈  𝑗𝑜𝑢𝑙𝑒 (𝐽), where ℎ= 6.626 070 15 × 10–34 𝐽· 𝑠 is the exact value of the Planck 
constant after the last SI reform (BIPM, 2018), and 𝜈 is the frequency of light (𝐻𝑧). 
 
The description of the environmental light exposure in terms of surface fluxes of 
energy or particles is of course entirely correct and, when given with enough spectral 
resolution and complementary information about the polarization state of the light, it 
provides a complete description of the light polluting field as pertinent for 
environmental and health sciences studies. However, expressing light pollution levels in 
terms of fluxes through surfaces has helped to frame light pollution as a somehow 
exceptional type of pollution, not clearly assimilable to the canonical air pollution forms 
(e.g. particulate matter of different sizes, ground-level ozone, carbon monoxide, sulfur 
dioxide, nitrogen dioxide, or lead), whose levels are normally expressed in terms of their 
volume concentrations in the environment.  
 
As a matter of fact, light pollution levels can be equivalenty expressed in terms of 
the volume concentration of anthropogenic photons (in 𝑝ℎ𝑜𝑡𝑜𝑛𝑠· 𝑚−3). This 
formulation 
gives 
the 
same 
quantitative 
results 
as 
the 
traditional 
radiometric/photometric descriptions in terms of surface flux densities and helps to 
highlight the fundamental similarity between light pollution and other pollution types. 
The quantitative relations linking the surface flux and the volume concentration 
formulations are explicited in this paper. Section 2 contains the main transformation 
equations and a brief analysis of their most relevant features. In section 3 we provide 
quantitative results of these transformations applied to two spectral bands of 
environmental interest: the human photopic (𝑉𝜆) and the Johnson-Cousins V (hereafter 
𝑉𝐽). Discussion and conclusions are summarized in sections 4 and 5, respectively.

## Page 4

4 
 
 2. Methods 
This section develops the main equations linking the surface flux and the volume 
concentration formulations. To that end, let us consider a small fragment d𝑆 of any 
surface of interest, e.g. the input pupil of the eye of an individual of a given species, 
some elementary patch of the skin or the ground, or the entrance aperture of a light 
monitoring device deployed in the field.  
 
The total radiant energy d𝑄 incident during the time d𝑡 on this surface element, 
propagating within a small cone of directions dΩ around the direction vector 𝛂 and 
contained in the spectral wavelength interval [𝜆, 𝜆+ d𝜆], can be written as: 
d𝑄= 𝐿𝜆(𝛂) cos 𝑧 d𝑆 dΩ d𝜆 d𝑡                                            (1) 
where 𝐿𝜆(𝛂) is the spectral radiance of the light field, generally given in energy units 
𝑊· 𝑚−2 · 𝑠𝑟−1 · 𝑛𝑚−1. The direction of propagation of the radiance, 𝛂(𝑧, 𝜙), is usually 
specified in a spherical reference frame whose polar axis 𝑍 is perpendicular to the 
surface d𝑆,  being 𝑧 the angle of propagation with respect to 𝑍 and 𝜙 the azimuth, 
measured from any freely chosen azimuth origin.  Other variables on which the radiance 
may depend (time, location, polarization of the light field) are not explicitly indicated in 
Eq.(1) for simplicity, but they should be kept in mind. 
 
The spectral radiance 𝐿𝜆(𝛂) is the basic radiometric quantity for environmental 
studies, in the sense that it contains the most disaggregate information about the 
environmental light conditions. From this quantity any other radiometric or photometric  
magnitude can be immediately calculated. For instance, the total radiance 𝐿(𝛂) exciting 
a retinal photoreceptor of sensitivity 𝑉(λ), where 𝑉(λ) is any generic spectral sensitivity 
band, coming from a source located in the direction 𝛂 within the eye's field of view is 
given by 
𝐿(𝛂) = ∫ 𝐿𝜆(𝛂) 𝑉(λ) d𝜆
∞
𝜆=0
                𝑊· 𝑚−2 · 𝑠𝑟−1                 (2) 
In a similar way, the irradiance 𝐸 within the 𝑉(λ)  band, that is, the power received per 
unit surface (which is the sum of the radiances arriving from all directions of the front-
facing hemisphere weighted by the band sensitivity and by the cosine of the propagation 
angles measured from the normal to the surface) can be straightforwardly calculated as 
𝐸= ∫∫ 𝐿𝜆(𝛂) 𝑉(λ) cos 𝑧 d𝜆
∞
𝜆=0
dΩ
Ω
               𝑊· 𝑚−2                  (3) 
 
According to Eq (1) the spectral radiance is an energy density, more precisely the 
energy density per unit time (power), cosine-projected unit area, unit solid angle around 
the direction of propagation, and unit spectral interval around λ. Any radiometric or 
photometric quantity of environmental relevance may be easily obtained by integrating

## Page 5

5 
 
the spectral radiance with the appropriate weighting functions over the corresponding 
integration variables. 
 
The radiance and irradiance, either continuous (based on 𝑊) or discrete (based on 
𝑝ℎ𝑜𝑡𝑜𝑛𝑠· 𝑠−1) are natively defined as flows of energy through surfaces. However, a 
fully equivalent and equally correct formulation of these radiometric quantities can be 
straightforwardly made in terms of volume concentrations of photons. To do so, let us 
recall that Eq.(1) can be rewritten in terms of photon numbers as 
d𝑄= 𝑛𝜆(𝛂) ℎ𝜈 dΩ d𝜆 d𝑉                                                  (4)  
where ℎ𝜈 is the energy in joules per photon (𝐽· 𝑝ℎ𝑜𝑡𝑜𝑛−1) and 𝑛𝜆(𝛂) is the number of 
photons per unit volume (𝑉), per unit solid angle around the propagation direction 𝛂 
and per unit spectral interval around 𝜆 (𝑛𝜆(𝛂) has units 𝑝ℎ𝑜𝑡𝑜𝑛𝑠· 𝑚−3 · 𝑠𝑟−1 · 𝑛𝑚−1). 
The factor d𝑉 is the atmospheric volume containing the photons that will impact on the 
surface d𝑆 propagating at the speed of light during the time d𝑡 along the direction 𝛂,  
which is inclined an angle 𝑧 with respect to the surface normal (Fig.1). The volume of 
this slanted cylinder of base d𝑆 is d𝑉=  d𝑆 𝑐 d𝑡cos 𝑧, where 𝑐= 299 792 458 𝑚· 𝑠−1 
is the exact value of the speed of light (BIPM, 2018).  
 
Figure 1. Geometry of the light propagation. The quantity 𝑛𝜆(𝛂) is the volume density 
of photons propagating towards the surface d𝑆 per unit solid angle along the direction 
𝛂 (at an angle 𝑧 with the normal to the surface) and per unit wavelength interval. The 
slanted cylinder volume is d𝑉=  d𝑆 𝑐 d𝑡cos 𝑧. 
 
Since the energy d𝑄 is the same in Eqs.(1) and (4), and 𝜈= 𝑐/𝜆 we get 
𝐿𝜆(𝛂) = ℎ𝑐2
𝜆𝑛𝜆(𝛂)                                                           (5) 
Equation (5) shows that the spectral radiance for each wavelength 𝜆 is directly 
proportional to 𝑛𝜆(𝛂), the angular and spectral density of the volume concentration of 
photons.

## Page 6

6 
 
 
This basic equivalence can be immediately transferred to aggregated radiometric 
magnitudes like the in-band radiance or the irradiance in Eqs. (2)-(3). The in-band 
radiance becomes: 
𝐿(𝛂) = ℎ𝑐2 ∫ 𝑛𝜆(𝛂) 𝑉(λ)
λ
 d𝜆
∞
𝜆=0
                𝑊· 𝑚−2 · 𝑠𝑟−1                (6) 
The standard practice for specifying the spectral sensitivity bands 𝑉(λ), including the 
transmission functions of photometric filters and the action spectra of several 
physiological process, is to normalize them to 1 at its maximum. This criterion can be 
kept in Eq.(6) by defining a dimensionless normalized spectral sensitivity band Λ(𝜆), 
derived from the original 𝑉(𝜆) as 
Λ(𝜆) =
𝑉(𝜆) 𝜆
⁄
[𝑉(𝜆) 𝜆
⁄ ]𝑚𝑎𝑥
≡𝑉(𝜆) 𝜆
⁄
𝐾0
                                        (7) 
where 𝐾0 = [𝑉(𝜆) 𝜆
⁄ ]𝑚𝑎𝑥 has dimensions of inverse length (𝑚−1). This allows rewriting 
the in-band radiance in the form 
𝐿(𝛂) = ℎ𝑐2𝐾0 ∫𝑛𝜆(𝛂) Λ(𝜆) d𝜆
∞
𝜆=0
                𝑊· 𝑚−2 · 𝑠𝑟−1                 (8) 
that can be read as  
𝐿(𝛂) = ℎ𝑐2𝐾0 𝑁(𝛂)                𝑊· 𝑚−2 · 𝑠𝑟−1                 (9) 
where 𝑁(𝛂) = ∫
𝑛𝜆(𝛂) Λ(𝜆) d𝜆
∞
𝜆=0
 is the volume concentration of photons of all 
wavelengths, weighted by Λ(𝜆),  propagating per unit solid angle in the direction 𝛂. 
Analogously we have for the irradiance 
𝐸= ℎ𝑐2𝐾0 ∫∫𝑛𝜆(𝛂) Λ(𝜆)
𝜆
d𝜆cos 𝑧dΩ 
Ω
          𝑊· 𝑚−2                  (10) 
which can be read as  
𝐸= ℎ𝑐2𝐾0 𝑁                                                              (11) 
where  
𝑁= ∫∫𝑛𝜆(𝛂) Λ(𝜆)
𝜆
d𝜆cos 𝑧dΩ =
Ω
 ∫𝑁(𝛂) cos 𝑧dΩ
Ω
                    (12) 
is the photon concentration per unit volume (𝑝ℎ𝑜𝑡𝑜𝑛𝑠· 𝑚−3) within the spectral band 
Λ(𝜆), propagating along all directions from the front-facing hemisphere (0 ≤𝑧≤
90°, 0 ≤𝜙< 360°;  Ω = 2𝜋 𝑠𝑟) towards the element of surface on which the irradiance 
is measured, weighted by the cosine of the propagation angle.

## Page 7

7 
 
3. Results 
To get some insights about these transformations, in this section we report their specific 
values for the human photopic spectral sensitivity band, 𝑉𝜆, and for the Johnson-Cousins 
𝑉𝐽. Similar calculations can be straightforwardly made for any other band of 
environmental or public health interest (see section 4). 
 
3.1 CIE 𝑉𝜆 photopic spectral sensitivity band 
 
The conversion between radiant units and luminous ones (i.e. radiant ones 
weighted by the spectral sensitivity of the human visual system and expressed in 
luminous units based on the 𝑐𝑑) is determined by the CIE photopic spectral sensitivity 
function 𝑉𝜆 (CIE, 1926) scaled by the constant 𝐾𝑐𝑑, the SI value for the luminous efficacy 
of monochromatic radiation of frequency 540 × 1012 Hz (i.e., 𝜆= 555 𝑛𝑚), defined as 
𝐾𝑐𝑑= 683 𝑙𝑚· 𝑊−1 (BIPM, 2018). Within this framework the luminance 𝐿𝑉(𝛂) of a 
light beam of in-band radiance 𝐿(𝛂) is given by  
𝐿𝑉(𝛂) = 683 𝐿(𝛂) = 683 ℎ𝑐2𝐾0 𝑁(𝛂)            𝑐𝑑· 𝑚−2            (13) 
and the illuminance 𝐸𝑉 corresponding to the in-band irradiance 𝐸 by 
𝐸𝑉= 683 𝐸= 683 ℎ𝑐2𝐾0 𝑁                          𝑙𝑥                     (14) 
 
For the CIE 𝑉𝜆(𝜆) band the function 𝑉𝜆(𝜆)/𝜆 attains its maximum at 𝜆= 𝜆0 =
 550.4 𝑛𝑚, resulting in 𝐾0 = 𝑉𝜆(𝜆0)/𝜆0 = 1.8090 × 106  𝑚−1. From these values the 
following conversion constants are obtained 
𝜇𝑉= 683 ℎ𝑐2𝐾0 =  7.3581 × 10−8    𝑙𝑥 𝑝𝑒𝑟 𝑝ℎ𝑜𝑡𝑜𝑛· 𝑚−3           (15) 
and  
𝜂𝑉=
1
683 ℎ𝑐2𝐾0
=  1.3590 × 107      𝑝ℎ𝑜𝑡𝑜𝑛𝑠· 𝑚−3 𝑝𝑒𝑟 𝑙𝑥            (16) 
These photon concentration conversion constants can also be expressed in any other 
convenient SI derived units, with less significant digits where practical or appropriate 
(e.g. 𝜂𝑉≈13.6 𝑝ℎ𝑜𝑡𝑜𝑛𝑠· 𝑐𝑚−3 𝑝𝑒𝑟 𝑙𝑥).  
 
The conversion constant 𝜇𝑉 in Eq.(15) can be interpreted relative to the normalized 
Λ(𝜆) band in an analogous way as the constant 𝐾𝑐𝑑= 683 𝑙𝑚· 𝑊−1 is interpreted 
relative to the CIE 𝑉𝜆(𝜆) band. Recall that the latter can be rewritten as 𝐾𝑐𝑑= 683 
𝑙𝑥 𝑝𝑒𝑟 𝑊· 𝑚−2. The illuminance in 𝑙𝑥 is calculated by adding (integrating) the incident 
spectral irradiance (in 𝑊· 𝑚−2 · 𝑛𝑚−1) across wavelengths, weighted by the 𝑉𝜆(𝜆) 
function. This provides the number of band-weighted 𝑊· 𝑚−2 that, multiplied by  𝐾𝑐𝑑, 
transforms into 𝑙𝑥. In a similar way, integrating (spectrally and angularly) the photon 
density 𝑛𝜆(𝛂) in Eq.(12) weighted by the Λ(𝜆) function provides the number of band-
weighted 𝑝ℎ𝑜𝑡𝑜𝑛𝑠· 𝑚−3, 𝑁, that after multiplication by 𝜇𝑉, transforms into 𝑙𝑥. It is 
important to keep in mind that 𝑁 is a band-weighted volume density: this means that

## Page 8

8 
 
two monochromatic radiations of wavelengths 𝜆1,  𝜆2, will produce an equal amount of 
illuminance (or of any other photometric luminous quantity) if their respective basic 
photon densities 𝑛𝜆(𝛂) in Eq.(4) are in the ratio 𝑛𝜆1(𝛂) 𝑛𝜆2(𝛂)
⁄
= Λ(𝜆2) Λ(𝜆1)
⁄
. This 
echoes the well-known fact that the same amount of illuminance can be obtained with 
two monochromatic radiations whose spectral irradiances are in the ratio 
𝐸(𝜆1) 𝐸(𝜆2)
⁄
= 𝑉𝜆(𝜆2) 𝑉𝜆(𝜆1)
⁄
. 
 
The in-band, cosine weighted photon volume concentration  𝜂𝑉  corresponding to 
1 𝑙𝑥, Eq.(16), is not as small as at a first glance these figures could suggest. This volume 
concentration is equivalent to an in-band photon surface flux density of 𝜂𝑉× 𝑐=
4.0743 × 1015 𝑝ℎ𝑜𝑡𝑜𝑛𝑠· 𝑠−1 · 𝑚−2 𝑝𝑒𝑟 𝑙𝑢𝑥 , consistent with the expected value. 
Recall that photons just need about 3.3 ns time to travel 1 m. Given a 1m x 1m  detector 
surface, photons span in that time a volume of 1 m3 that contains 1.3590 × 107 in-band, 
cosine weighted photons per lux incident on that surface. 
 
3.2 Johnson-Cousins 𝑉𝐽 band 
 
Another spectral band widely used in environmental light pollution monitoring and 
research is the Johnson-Cousins V (Bessell, 1999; Bessell and Murphy, 2012), here 
denoted 𝑉𝐽(𝜆). This band is located in the central region of the optical spectrum, has a 
bandwidth of 90.89 nm and peaks at 529 nm with a normalized maximum value equal 
to 1. The Johnson-Cousins 𝑉𝐽 band has been extensively used as standard for reporting 
the anthropogenic brightness of the night sky, and several key measuring devices (Hänel 
et al., 2018) and iconic light pollution quantitative models (Falchi et al., 2016) are 
designed and built based on it.  
 
The photon volume concentration corresponding to the irradiance in this band can 
be easily calculated from Equation (11), taking into account that in this case the function 
𝑉𝐽(𝜆)/𝜆 peaks at 𝜆0 =  526.5 𝑛𝑚, resulting in 𝐾0 = 𝑉𝐽(𝜆0)/𝜆0  = 1.8959 × 106  𝑚−1. 
This immediately leads to the conversion factors  
𝜇𝐽= ℎ𝑐2𝐾0 = 0.1129 × 10−9    𝑊· 𝑚−2 𝑝𝑒𝑟 𝑝ℎ𝑜𝑡𝑜𝑛· 𝑚−3              (17) 
𝜂𝐽=
1
 ℎ𝑐2𝐾0
=  8.8568 × 109      𝑝ℎ𝑜𝑡𝑜𝑛𝑠· 𝑚−3 𝑝𝑒𝑟 𝑊· 𝑚−2             (18) 
 
As an example of the practical significance of this conversion factors, Figure 2 shows 
the photon volume concentrations 𝑁 in 𝑙𝑜𝑔10 (𝑝ℎ𝑜𝑡𝑜𝑛𝑠· 𝑚−3) associated with the 
ground level horizontal irradiance produced by the artificial brightness of the night sky, 
in an area comprising the Iberian Peninsula, Northern Maghreb (Northern Algeria, 
Morocco, and Tunisia), Southern France, and Balearic Islands. The map, in log decimal 
grayscale, shows the large increase of the volume concentration of anthropogenic 
photons in and around metropolitan areas, as well as its pervasive presence in wide 
inhabited regions, including the coastal waters of the Atlantic Ocean and the

## Page 9

9 
 
Mediterranean sea. The anthropogenic sky irradiance has been computed by following 
the procedures and methods described in Falchi and Bará (2021). 
 
Note that in addition to the photon concentrations produced by the artificial light 
scattered in the atmosphere, shown in Fig. 2, there is also in many places (urban regions, 
areas surrounding roadways, industrial installations,...) a noticeable contribution of 
direct radiance from the nearby streetlights, whose associated photon volume 
concentrations would add to the ones shown in this map. 
 
Figure 2. Ground-level photon volume concentrations (𝑁) in the Johnson-Cousins 𝑉𝐽 
band, associated with the horizontal irradiance produced by the artificial brightness of 
the night sky, in an area comprising the Iberian Peninsula, Northern Maghreb (Northern 
Algeria, Morocco, and Tunisia), Southern France, and Balearic Islands. CRS: EPSG:25830 
- ETRS89 / UTM zone 30N. Pixel width 409.44 m. Grayscale in 𝑙𝑜𝑔10 (𝑝ℎ𝑜𝑡𝑜𝑛𝑠· 𝑚−3). 
 
4. Discussion 
In the above sections the correspondence between the usual radiometric and 
photometric quantities expressed as surface flux densities and their associated photon 
volume concentrations has been explicited in a general way (section 2) and 
particularized for the spectral sensitivity of the human visual system and the Johnson-
Cousins 𝑉𝐽 band (section 3). The same approach can be applied to any other spectral 
sensitivity band of environmental or public health interest, as e.g. different types of 
opsins (Govardovskii et al., 2000), wildlife action spectra (van Grunsven et al., 2014; 
Donners et al, 2018; Longcore et al., 2018; Nilsson and Smolka, 2021), or the -opic 
sensitivities of human retinal photoreceptors mediating non-image forming effects of 
light, relevant for hormone regulation and physiological rhythms synchronization, 
among others (CIE, 2018; Schlangen and Price, 2021).

## Page 10

10 
 
 
The conceptualization of light pollution as an increased volume concentration of 
polluting particles in the nocturnal environment above the expected natural values, first 
presented and developed in two seminal papers by Cinzano and Falchi (2012, 2014), can 
be easily extended to any of the above quoted bands by using Eqs. (8) and (10) of this 
paper. Reference values for the natural baseline in diverse bands may be found in 
Masana et al. (2021, 2022). 
 
The proposed description does not rely on a unique total volume density of 
photons, but on the volume density of the subset of photons relevant for the 
photometric magnitude under study, which in general will be different for each 
magnitude. In case of the spectral radiance in a given direction (𝛂), the relevant photon 
volume density is 𝑛𝜆(𝛂), Eq.(4), i.e. that of the photons propagating per unit solid angle 
and unit spectral interval along the prescribed direction. In case of the total 
radiance/luminance in that direction, the relevant photon volume density is 𝑁(𝛂), 
defined in Eq.(9) after an in-band spectral integration. In case of the total 
irradiance/illuminance it is the volume density 𝑁 of the photons propagating in all 
directions (cosine and band-weighted) towards the chosen elementary surface, defined 
in Eq.(12). If the radiometric magnitude under study were the total radiant energy within 
a volume, the relevant density would be related to the total number of photons per unit 
volume. Other metrics may require their own density definitions (see, e.g. Jechow and 
Hölker, 2019). The main takeaway message is that every radiometric/photometric 
magnitude can be equivalently expressed in terms of the volume density of the 
appropriate subset of photons. Specifying volume densities of  different subsets of 
photons (classified by their properties) is analogous to specifying volume densities of 
different subsets of particulate matter (classified by their properties, e.g. sizes as in 
PM2.5, PM10, etc.). The concentration of PM2.5 is not the total concentration of 
material particles in the air, but the concentration of the particles of a given size range, 
relevant for a definite purpose; the same approach is followed here when defining the 
photon concentrations described in this paper. 
 
The formulation of environmental light exposures in terms of volume 
concentrations of photons is a complement, rather than a substitute for the traditional 
specification of lighting levels in terms of radiometric and photometric surface fluxes. 
However, future light pollution regulations may take advantage of this approach to 
specify exposure limits (also) in terms of maximum allowed atmospheric concentrations 
of anthropogenic light particles, seamlessly unifying them with the current regulations 
of other well-known atmospheric pollutants. 
 
5. Conclusions 
The light pollution levels in the nocturnal environment can be rigorously expressed in 
terms of the volume concentration of anthropogenic light particles. The basic equations

## Page 11

11 
 
of this formulation and their application to any spectral sensitivity band, including visual 
and non-visual ones of environmental and public health relevance, are described in this 
work. This equivalent formulation of the light pollution exposures, consistent with the 
basic physical processes of emission, scattering, and absorption of light, provides a 
unified framework to understand and manage artificial light at night as a conventional 
air pollutant.  
 
 
Acknowledgements 
Any scientific research work benefits from multiple exchanges with fellow scientists, and 
this is no exception. Special thanks are due, among others, to Raul Lima and Martin 
Pawley for insightful comments and criticisms on light pollution issues. Anonymous 
reviewers provided very useful suggestions that helped to improve this paper. Any 
remaining error of this paper is of course the sole responsibility of the authors. 
 
Funding sources 
CB acknowledges funding from Xunta de Galicia/FEDER, grant ED431B 2020/29. 
 
 
References 
American Medical Association, Ama, 2012. Light Pollution: adverse health effects of 
nighttime lighting. Chicago, Illinois (USA. In: Proceedings of the American 
MedicalAssociation House of Delegates, 161st Annual Meeting, pp. 265–279. 
Online: 
https://www.ama-assn.org/sites/ama-assn.org/files/corp/media-
browser/public/hod/a12-csaph-reports_0.pdf. 
Bará, S., 2016. Anthropogenic disruption of the night sky darkness in urban and rural 
areas. R. Soc. Open Sci. 3, 160541 https://doi.org/10.1098/rsos.160541. 
Bessell, M.S., 1990. UBVRI Passbands, vol. 102. Publications of the Astronomical Society 
of the Pacific, pp. 1181–1199. https://doi.org/10.1086/132749. 
Bessell, M., Murphy, S., 2012. Spectrophotometric libraries, revised photonic passbands, 
and zero points for UBVRI, hipparcos, and tycho photometry. Publ. Astron. Soc. Pac. 
124, 140–157. 
BIPM, 2018. Resolution 1 of the 26th CGPM: on the revision of the international system 
of units (SI). https://www.bipm.org/en/committees/cg/cgpm/26-2018/resolution-
1. (Accessed 11 April 2022).

## Page 12

12 
 
Boyce, P., 2022. Light, lighting and human health. Light. Res. Technol. 54 (2), 101–144. 
https://doi.org/10.1177/14771535211010267. 
Brown, T.M., Brainard, G.C., Cajochen, C., Czeisler, C.A., Hanifin, J.P., Lockley, S.W., et 
al., 2022. Recommendations for daytime, evening, and nighttime indoor light 
exposure to best support physiology, sleep, and wakefulness in healthy adults. PLoS 
Biol. 20 (3), e3001571 https://doi.org/10.1371/journal.pbio.3001571. 
Cayrel, R., 1979. Identification and Protection of Existing and Potential Observatory 
Sites. Trans. Int. Astron. Union 17 (1), 215–223. https://doi.org/10.1017/ 
S0251107X00010798. 
CIE, 1926. Commission Internationale de l’Eclairage Proceedings, 1924. Cambridge 
University Press, Cambridge. 
CIE, 2018. Commission Internationale de l’Eclairage. CIE System for Metrology of Optical 
Radiation for ipRGC-Influenced Responses to Light. Publication CIE S 026/E. 
https://doi.org/10.25039/S026.2018. 
Cinzano, P., Falchi, F., 2012. The propagation of light pollution in the atmosphere. Mon. 
Not. Roy. Astron. Soc. 427, 3337–3357. https://doi.org/10.1111/j.1365-
2966.2012.21884.x. 
Cinzano, P., Falchi, F., 2014. Quantifying light pollution. J. Quant. Spectrosc. Radiat. 
Transf. 139, 13–20. https://doi.org/10.1016/j.jqsrt.2013.11.020. 
Cinzano, P., Falchi, F., Elvidge, C., 2001. The first world atlas of the artificial night sky 
brightness. 
Mon. 
Not. 
Roy. 
Astron. 
Soc. 
328, 
689–707. 
https://doi.org/10.1046/j.1365-8711.2001.04882.x. 
Convention on the Conservation of Migratory Species of Wild Animals, 2020. Light 
pollution guidelines for wildlife. Thirteenth meeting of the conference of the parties 
to CMS , 15.02.2020. India, CMS Resolution 13.5. Publish date 08 April 2020 1–2. 
https://www.cms.int/sites/default/files/document/cms_cop13_res.13.5_light-
pollution-guidelines_e.pdf. (Accessed 5 August 2022). 
Davies, T.W., Bennie, J., Inger, R., Gaston, K.J., 2013. Artificial light alters natural regimes 
of night-time sky brightness. Sci. Rep. 3, 1722. https://doi.org/10.1038/srep01722. 
Davis, S., Mirick, D.K., Stevens, R.G., 2001. Night shift work, light at night, and risk of 
breast 
cancer. 
J. 
Natl. 
Cancer 
Inst. 
93, 
1557–1562. 
https://doi.org/10.1093/jnci/93.20.1557. 
Donners, M., van Grunsven, R.H.A., Groenendijk, D., van Langevelde, F., Bikker, J.W., 
Longcore, T., Veenendaal, E.M., 2018. Colors of attraction: modeling insect flight to 
light behavior. J. Exp. Zool. 329, 434–440. https://doi.org/10.1002/jez.2188.

## Page 13

13 
 
Einstein, A., 1905. Über einen die Erzeugung und Verwandlung des Lichtes betreffenden 
heuristischen Gesichtspunkt [On a Heuristic Point of View about the Creation and 
Conversion of Light]. Ann. Phys. 17 (6), 132–148 (in German). 
European Union, 2018. EU Green Public Procurement criteria for road lighting andtraffic 
signals. 
http://ec.europa.eu/environment/gpp/pdf/toolkit/181210_EU_GPP_criteria_road
_lighting.pdf. 
Falchi, F., Bará, S., 2021. Computing light pollution indicators for environmental 
assessment. Nat Sci. e10019. https://doi.org/10.1002/ntls.10019. 
Falchi, F., Cinzano, P., Duriscoe, D., Kyba, C.C.M., Elvidge, C.D., Baugh, K., Portnov, B. A., 
Rybnikova, N.A., Furgoni, R., 2016. The new world atlas of artificial night sky 
brightness. Sci. Adv. 2, e1600377 https://doi.org/10.1126/sciadv.1600377. 
García-Sáenz, A., de Miguel, A.S., Espinosa, A., Valentin, A., Aragones, N., Llorca, J., 
Amiano, P., Sanchez, V.M., Guevara, M., Capelo, R., et al., 2018. Evaluating the 
association between artificial light-at-night exposure and breast and prostate 
cancer risk in Spain (MCC-Spain study). Environ. Health Perspect. 126 (4), 047011 
https://doi.org/10.1289/EHP1837. 
Garstang, R.H., 1989. Night-sky Brightness at Observatories and Sites, vol. 101. 
Publications of the Astronomical Society of the Pacific, pp. 306–329. 
https://doi.org/10.1086/132436. 
Gaston, K.J., Ackermann, S., Bennie, J., Cox, D.T.C., Phillips, B.B., Sánchez de Miguel, A., 
Sanders, D., 2021. Pervasiveness of biological impacts of artificial light at night. 
Integr. Comp. Biol. 61 (3), 1098–1110. https://doi.org/10.1093/icb/icab145. 
Govardovskii, V.I., Fyhrquist, N., Reuter, T., Kuzmin, D.G., Donner, K., 2000. In search of 
the 
visual 
pigment 
template. 
Vis. 
Neurosci. 
17 
(4), 
509–528. 
https://doi.org/10.1017/s0952523800174036. 
Green, R.F., Luginbuhl, C.B., Wainscoat, R.J., et al., 2022. The growing threat of light 
pollution to ground-based observatories. Astron. AstroPhys. Rev. 30, 1. 
https://doi.org/10.1007/s00159-021-00138-3. 
Haim, A., Portnov, B., 2013. Light Pollution as a New Risk Factor for Human Breast and 
Prostate Cancers. Springer, Heidelberg. https://doi.org/10.1007/978-94-007-6220-
6. 
Hänel, A., Posch, T., Ribas, S.J., Aubé, M., Duriscoe, D., Jechow, A., Kollath, Z., Lolkema, 
D.E., Moore, C., Schmidt, N., Spoelstra, H., Wuchterl, G., Kyba, C.C.M., 2018. 
Measuring night sky brightness: methods and challenges. J. Quant. Spectrosc. 
Radiat. Transfer 205, 278–290. https://doi.org/10.1016/j.jqsrt.2017.09.008.

## Page 14

14 
 
Hölker, F., Wolter, C., Perkin, E.K., Tockner, K., 2010. Light pollution as a biodiversity 
threat. Trends Ecol. Evol. 25, 681–682. https://doi.org/10.1016/j.tree.2010.09.007. 
IARC Monographs Vol 124 group, Ward, E.M., Germolec, D., Kogevinas, M., et al., 
2019.Carcinogenicity of night shift work. Lancet Oncol. 20 (8), 1058–1059. 
https://doi.org/10.1016/S1470-2045(19)30455-3. 
International Union for Conservation of Nature, IUCN, 2021. Taking Action to 
ReduceLight Pollution. IUCN World Conservation Congress. Resolution 084. 
https://www.iucncongress2020.org/motion/084. 
Jechow, A., Hölker, F., 2019. How dark is a river? Artificial light at night in aquatic systems 
and the need for comprehensive night-time light measurements. Wiley 
Interdisciplinary Reviews: Water 6 (6), e1388. https://doi.org/10.1002/wat2.1388. 
Kyba, C.C.M., Kuester, T., Sánchez de Miguel, A., Baugh, K., Jechow, A., Hölker, F., 
Bennie, J., Elvidge, C.D., Gaston, K.J., Guanter, L., 2017. Artificially lit surface of Earth 
at night increasing in radiance and extent. Sci. Adv. 3, e1701528 
https://doi.org/10.1126/sciadv.1701528. 
Longcore, T., Rich, C., 2004. Ecological light pollution. Front. Ecol. Environ. 2, 191–198. 
https://doi.org/10.1890/1540-9295(2004)002[0191:ELP]2.0.CO;2. 
Longcore, T., Rodríguez, A., Witherington, B., Penniman, J.F., Herf, L., Herf, M., 2018. 
Rapid assessment of lamp spectrum to quantify ecological effects of light at night. 
J. Exp. Zool. 329, 511–521. https://doi.org/10.1002/jez.2184. 
Marín, C., Jafari, J., 2008. StarLight: A Common Heritage; StarLight Initiative La Palma 
Biosphere Reserve. Instituto De Astrofísica De Canarias, Government of The Canary 
Islands, Spanish Ministry of The Environment, UNESCO-MaB, Canary Islands, Spain. 
Masana, E., Carrasco, J.M., Bará, S., Ribas, S.J., 2021. A multi-band map of the natural 
night sky brightness including Gaia and Hipparcos integrated starlight. Monthly 
Notices 
of 
the 
Royal 
Astronomical 
Society 
501, 
5443–5456. 
doi: 
10.1093/mnras/staa4005 
Masana, E., Bará, S., Carrasco, J.M., Ribas, S.J., 2022. An enhanced version of the Gaia 
map of the brightness of the natural sky. International Journal of Sustainable 
Lighting 24 (1), 1–12. https://doi.org/10.26607/ijsl.v24i1.119. 
Nilsson, D.-E., Smolka, J., 2021. Quantifying biologically essential aspects 
ofenvironmental 
light. 
J. 
R. 
Soc. 
Interface 
18, 
20210184. 
https://doi.org/10.1098/rsif.2021.0184. 
Nilsson, D.-E., Smolka, J., Bok, M., 2022. The vertical light-gradient and its 
potentialimpact on animal distribution and behavior. Front. Ecol. Evol. 10, 951328 
https://doi.org/10.3389/fevo.2022.951328.

## Page 15

15 
 
Rich, C., Longcore, T. (Eds.), 2006. Ecological Consequences of Artificial Night Lighting. 
Island Press, Washington, D.C. 
Russart, K.L.G., Nelson, R.J., 2018. Light at night as an environmental endocrine 
disruptor. 
Physiol. 
Behav. 
190, 
82–89. 
https://doi.org/10.1016/j.physbeh.2017.08.029. 
Schlangen, L.J.M., Price, L.L.A., 2021. The lighting environment, its metrology, and 
nonvisual 
responses. 
Front. 
Neurol. 
12, 
624861 
https://doi.org/10.3389/fneur.2021.624861. 
Smolensky, M.H., Sackett-Lundeen, L.L., Portaluppi, F., 2015. Nocturnal light pollution 
and underexposure to daytime sunlight: complementary mechanisms of circadian 
disruption and related diseases. Chronobiol. Int. 32 (8), 1029–1048. 
https://doi.org/10.3109/07420528.2015.1072002. 
Stevens, R.G., Brainard, G.C., Blask, D.E., Lockley, S.W., Motta, M.E., 2014. Breast cancer 
and circadian disruption from electric lighting in the modern world. CA A Cancer J. 
Clin. 64, 207–218. https://doi.org/10.3322/caac.21218. 
Svechkina, A., Portnov, B.A., Trop, T., 2020. The impact of artificial light at night on 
human and ecosystem health: a systematic literature review. Landsc. Ecol. 35, 
1725–1742. https://doi.org/10.1007/s10980-020-01053-1. 
United Nations, 1996. 1979 Convention on Long-Range Transboundary Air Pollution and 
its Protocols [E/]ECE/EB.AIR/50. UN, New York ; Geneva (last accessed May 10th, 
2022). https://digitallibrary.un.org/record/237573?ln=en. 
United Nations, 2018. Report of the International Law Commission. Seventieth Session 
(30 April 1 June and 2 July 10 August 2018) General Assembly, Official 
Records,Seventy Third Session. UN, p. 171. Supplement No. 10 (A/73/10), VI. 
Protection of the atmosphere. https://legal.un.org/ilc/reports/2018/. (Accessed 10 
May 2022). 
van Grunsven, R.H.A., Donners, M., Boekee, K., Tichelaar, I., van Geffen, K.G., 
Groenendijk, D., Berendse, F., Veenendaal, E.M., 2014. Spectral composition of light 
sources and insect phototaxis, with an evaluation of existing spectral response 
models. J. Insect Conserv. 18 (2), 225–231. https://doi.org/10.1007/s10841-014-
9633-9. 
Walker, M.F., 1970. The California site survey. Publ. Astron. Soc. Pac. 82, 672–698. 
https://www.jstor.org/stable/40674892.
