#/bin/sh
# Build script for Tuxedo drivers
# Builts: tuxedo-drivers-kmod-common, kmod-tuxedo-drivers (for your kernel) and akmod-tuxedo-drivers

# Check if the kernels parameter is provided, if not, default to uname -r
if [ -z "$1" ]; then
  kernels=$(uname -r)
else
  kernels=$1
fi

echo "--> Copying spec files to ~/rpmbuild/SPECS/"
cp ./tuxedo-drivers-kmod.spec ~/rpmbuild/SPECS/
cp ./tuxedo-drivers-kmod-common.spec ~/rpmbuild/SPECS/

cd ~/rpmbuild/SPECS/

echo "--> Installing dependencies"
spectool -g -R tuxedo-drivers-kmod.spec

#rm ~/rpmbuild/RPMS/* -rf

echo "--> Building RPMs"
rpmbuild -ba tuxedo-drivers-kmod-common.spec
rpmbuild -ba tuxedo-drivers-kmod.spec
rpmbuild -ba tuxedo-drivers-kmod.spec --define "kernels ${kernels}"

echo "--> Listing RPMs"
tree ~/rpmbuild/RPMS/
