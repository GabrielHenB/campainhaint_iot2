#pacotes pip -U cmake dlib face-recoginition opencv-python numpy matplotlib setuptools
import cv2
import  face_recognition as fr

def reconhecimento(image, image2):
    try:
        #print(image)
        imgElon = fr.load_image_file(image)
        imgElon = cv2.cvtColor(imgElon,cv2.COLOR_BGR2RGB)
        imgElonTest = fr.load_image_file(image2)
        imgElonTest = cv2.cvtColor(imgElonTest,cv2.COLOR_BGR2RGB)

        faceLoc = fr.face_locations(imgElon)[0]
        cv2.rectangle(imgElon,(faceLoc[3],faceLoc[0]),(faceLoc[1],faceLoc[2]),(0,255,0),2)

        encodeElon = fr.face_encodings(imgElon)[0]
        encodeElonTest = fr.face_encodings(imgElonTest)[0]

        comparacao = fr.compare_faces([encodeElon],encodeElonTest)
        distancia = fr.face_distance([encodeElon],encodeElonTest)

        # Mostra o resultado da comparacao e a medida de distancia, por fim exibindo as duas

        print(comparacao,distancia)
        #cv2.imshow('A Base',imgElon)
        #cv2.imshow('A Testada',imgElonTest)
        # Aguarde com a janela
        #cv2.waitKey(0)
        return comparacao[0]
    except Exception as excecao:
        print("ERRO NO RECONHECIMENTO = " + excecao)
        return None

#reconhecimento('igor2.jpg', 'igor1.jpg')
#reconhecimento('gabrielbase.jpeg','gabrielTeste.jpg')