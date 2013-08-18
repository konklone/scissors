Vagrant.configure("2") do |config|
  config.vm.box = 'debian-wheezy'
  config.vm.box_url = 'http://weblinksdca.s3.amazonaws.com/debian-wheezy.box'
  config.vm.provision :shell, :path => "vagrant.sh"
  config.vm.network :private_network, ip: "192.168.50.4"
  config.vm.network :forwarded_port, guest: 49154, host: 49154

end