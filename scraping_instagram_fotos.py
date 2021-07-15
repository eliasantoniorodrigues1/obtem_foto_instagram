from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from datetime import datetime
from time import sleep

# Others library
import os
import wget
import credentials


def navegar(driver, url):
    driver.get(url)


def efetua_login(driver, input_username, input_password, btn_submit, btn_not_now, usuario, senha):
    # Captura os elementos da página de Login e senha.
    username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, input_username)))
    password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, input_password)))

    # Limpa os input boxes
    username.clear()
    password.clear()

    # Clica e faz o login
    username.send_keys(usuario)
    password.send_keys(senha)
    log_in = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, btn_submit))).click()

    # Desabilita mensagens após logar
    not_now = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, btn_not_now))).click()

    not_now2 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, btn_not_now))).click()


def pesquisa(driver, input_searchbox, keyword, tot_img, path):
    ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
    ignored_exceptions = ignored_exceptions
    # Clicar no botão de pesquisa e procurar por uma hashtag
    searchbox = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, input_searchbox)))
    searchbox.clear()
    searchbox.send_keys(keyword)
    searchbox.send_keys(Keys.RIGHT)
    sleep(1)
    searchbox.send_keys(Keys.ARROW_DOWN)
    sleep(1)
    searchbox.send_keys(Keys.ENTER)
    sleep(1)
    # Executa a rolagem da barra até o final da tela
    for i in range(1, tot_img):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print(i)
    images = driver.find_elements_by_tag_name('img')
    images = [image.get_attribute('src') for image in images]
    salva_fotos(images, path, keyword)

    driver.quit()

    return images


def cria_diretorio(keyword):
    # Criando o diretório para salvar as imagens
    path = os.getcwd()
    path = os.path.join(path, keyword[1:])
    try:
        os.mkdir(path)
    except Exception as e:
        os.remove(path)
        os.mkdir(path)

    return path


def salva_fotos(images, path, keyword):
    # Baixando imagen por imagem e salvando no diretório com nome da hashtag
    timestamp = datetime.timestamp(datetime.now())
    counter = 0
    for k, image in enumerate(images):
        save_as = os.path.join(path, keyword[1:] + '_' + str(counter) + '_' 
                                                    + str(timestamp) + ".jpg")
        print(f'Salvando foto {k}. Link: {image}')
        wget.download(image, save_as)
        counter += 1


if __name__ == '__main__':
    # ----- ENTRADA DE DADOS ----- #
    text_driver = 'Driver/chromedriver.exe'
    driver = webdriver.Chrome(text_driver)
    url = 'https://www.instagram.com/'
    usuario = credentials.user_login
    senha = credentials.user_password
    palavra_chave = "dmouraplanejados"
    total_imgs = 50

    # Botões do Site:
    input_username = "input[name='username']"
    input_password = "input[name='password']"
    input_searchbox = "//input[@placeholder='Pesquisar']"
    btn_submit = "button[type='submit']"
    btn_not_now = "//button[contains(text(), 'Agora não')]"

    # ----- AÇÕES ----- #
    navegar(driver, url)
    efetua_login(driver, input_username, input_password, btn_submit,
                                         btn_not_now, usuario, senha)
    caminho = cria_diretorio(palavra_chave)
    pesquisa(driver, input_searchbox, palavra_chave, total_imgs, caminho)

    # salva_fotos(lista, caminho, palavra_chave)
    print(f'Fotos de {palavra_chave} salvas em ({caminho}) com sucesso!')
