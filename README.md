Otonom Robot Navigasyon ve QR Doğrulama Projesi

Bu proje, TurtleBot3 robotunun AWS Bookstore simülasyon ortamında otonom olarak belirlenen hedeflere gitmesini ve her hedef noktasındaki QR kodları kamerasıyla okuyarak doğrulamasını sağlayan bir ROS paketidir.
Kurulum Adımları

1. Gerekli Sistem Kütüphanelerini Kurun:
QR okuma ve oluşturma işlemleri için gerekli olan görüntü işleme paketlerini sisteminize yükleyin:
Bash

sudo apt update
sudo apt install libzbar0 -y
sudo apt install python3-pip -y
pip3 install pyzbar qrcode[pil]

2. Projeyi Çalışma Alanınıza Ekleyin:
Bu repoyu ROS çalışma alanınızın (örneğin ~/catkin_ws/src veya ~/final_ws/src) içine indirin.

3. 3D QR Modellerini Gazebo'ya Tanıtın:
Proje içindeki models/ klasöründe bulunan QR kod tabelalarını, Gazebo'nun modelleri okuduğu gizli dizine kopyalayın:
Bash

cp -r models/* ~/.gazebo/models/

4. Çalışma Alanını Derleyin:
Çalışma alanınızın ana dizinine dönüp projeyi derleyin ve terminali güncelleyin:
Bash

cd ~/final_ws
catkin_make
source devel/setup.bash

-----Çalıştırma Komutları-----

Sistemi tam otonom şekilde çalıştırmak için sırasıyla 3 ayrı terminal açın ve her birinde source devel/setup.bash komutunu çalıştırdıktan sonra aşağıdaki launch dosyalarını başlatın:

1. Simülasyonu Başlatma:
Gazebo dünyasını ve TurtleBot3 robotunu ortama yükler.
Bash

roslaunch final_proje_repo simulation.launch

2. Navigasyon ve Harita Sistemini Başlatma:
Önceden çıkarılmış haritayı ve RViz'i başlatır.
(Not: RViz açıldığında otonom sürüşün başlayabilmesi için üst menüden "2D Pose Estimate" butonunu kullanarak robotun haritadaki ilk konumunu işaretlemeniz zorunludur).
Bash

roslaunch final_proje_repo navigation.launch

3. Görev Yöneticisini Başlatma (Tam Otonom Mod):
Bu komut sırasıyla 3D tabelaları robotun karşısına yerleştirir, canlı kamerayı açar ve robotu hedeflere yollar.
Bash

roslaunch final_proje_repo task_manager.launch

Kullanılan ROS Yapıları

Proje hiyerarşisinde modülerliği sağlamak adına aşağıdaki ROS iletişim yapıları kullanılmıştır:
1. Topics (Konular)

    /camera/rgb/image_raw : TurtleBot3 kamerasından gelen anlık ham görüntü verisini almak için qr_reader düğümü tarafından Subscribe (Abone) olunmuştur.

    /detected_qr : Kameranın çözdüğü QR kod metinlerini görev yöneticisine (beyne) iletmek için qr_reader düğümü tarafından oluşturulmuş özel bir haberleşme kanalıdır. qr_reader bu kanala Publish (Yayın) yapar, task_manager ise bu kanala Subscribe (Abone) olur.

2. Services (Servisler)

    /gazebo/spawn_sdf_model : Görev noktalarındaki 3D QR tabelalarını Gazebo ortamına otonom olarak (robotun hedefine göre matematiksel açı hesaplayarak) yerleştirmek için spawn_qrs.py betiği tarafından çağrılan Gazebo servisidir.

3. Actions (Eylemler)

    move_base : Robotun mission.yaml dosyasından okunan hedef koordinatlara (x, y, qz, qw) otonom navigasyonla gidebilmesi için task_manager.py içinde SimpleActionClient kullanılarak çağrılan aksiyon yapısıdır. Robot hedefe ulaşana kadar beklenir ve başarı/başarısızlık durumu eylem sonucuna göre değerlendirilir.
