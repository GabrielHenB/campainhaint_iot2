#pacotes pip -U cmake dlib face-recoginition opencv-python numpy matplotlib setuptools
import cv2
import  face_recognition as fr

def reconhecimento(image, image2):
    try:
        #print(image)
        print(f"RECONHECIMENTO: Base = f{image}")
        print(f"RECONHECIMENTO: Alvo = f{image2}")

        imgElon = fr.load_image_file(image)
        imgElon = cv2.cvtColor(imgElon,cv2.COLOR_BGR2RGB)
        imgElonTest = fr.load_image_file(image2)
        imgElonTest = cv2.cvtColor(imgElonTest,cv2.COLOR_BGR2RGB)

        faceLoc = fr.face_locations(imgElon)[0]

        # Se nenhum rosto for encontgado nao continue
        if not faceLoc:
            print("Nenhuma face detectada na imagem de base.")
            print(faceLoc)
            return None

        cv2.rectangle(imgElon,(faceLoc[3],faceLoc[0]),(faceLoc[1],faceLoc[2]),(0,255,0),2)

        #encodeElon = fr.face_encodings(imgElon)[0]
        encodeElon = fr.face_encodings(imgElon)

        if not encodeElon:
            print("Não foi possível codificar a face na imagem de base.")
            print(encodeElon)
            return None
        
        encodeElon = encodeElon[0]

        #encodeElonTest = fr.face_encodings(imgElonTest)[0]
        encodeElonTest = fr.face_encodings(imgElonTest)

        if not encodeElonTest:
            print("Não foi possível codificar a face na imagem de teste.")
            print(encodeElonTest)
            return None

        encodeElonTest = encodeElonTest[0]

        comparacao = fr.compare_faces([encodeElon],encodeElonTest)
        distancia = fr.face_distance([encodeElon],encodeElonTest)

        # Mostra o resultado da comparacao e a medida de distancia, por fim exibindo as duas

        print(comparacao,distancia)
        #cv2.imshow('A Base',imgElon)
        #cv2.imshow('A Testada',imgElonTest)
        # Aguarde com a janela
        #cv2.waitKey(0)
        return comparacao[0]
    except IndexError as index_error:
        print("Erro de índice: Nenhuma face detectada na imagem.")
        return None
    except Exception as excecao:
        print("ERRO NO RECONHECIMENTO = {}".format(excecao))
        return None

#reconhecimento('igor2.jpg', 'igor1.jpg')
#reconhecimento('gabrielbase.jpeg','gabrielTeste.jpg')