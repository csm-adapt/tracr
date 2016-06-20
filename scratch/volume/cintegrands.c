#include <math.h>

double truncated_volume(int n, double args[n]) {
  // Integrand for calculating the volume of a truncated sphere.
  // INPUTS
  //   phi: polar angle
  //   theta: azimuthal angle
  //   r: radius
  //   alpha: "tightness" of the hyperbolic tangent
  //   xmin, ymin, zmin, xmax, ymax, zmax: lower and upper bounds
  //
  // OUTPUT
  //   volume of differential element

  // integration variables, inner to outer
  double phi = args[0];
  double theta = args[1];
  double r = args[2];
  // parameters
  double alpha = args[3];
  double xmin = args[4];
  double ymin = args[5];
  double zmin = args[6];
  double xmax = args[7];
  double ymax = args[8];
  double zmax = args[9];
  // derived quantities
  double rcf = r*cos(phi);
  double rsf = r*sin(phi);
  double cq = cos(theta);
  double sq = sin(theta);
  // boundary conditions as tanh functions
  double xfactor = 0.0;
  double yfactor = 0.0;
  double zfactor = 0.0;
  double lower = 0.0;
  double upper = 0.0;

  lower = (1. + tanh(alpha*(rsf*cq - xmin)))/2.;
  upper = 1. - (1. + tanh(alpha*(rsf*cq - xmax)))/2.;
  xfactor = lower * upper;

  lower = (1. + tanh(alpha*(rsf*sq - ymin)))/2.;
  upper = 1. - (1. + tanh(alpha*(rsf*sq - ymax)))/2.;
  yfactor = lower * upper;

  lower = (1. + tanh(alpha*(rcf - zmin)))/2.;
  upper = 1. - (1. + tanh(alpha*(rcf - zmax)))/2.;
  zfactor = lower * upper;

  return xfactor*yfactor*zfactor*r*rsf;
}
