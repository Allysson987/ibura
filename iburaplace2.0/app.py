
import requests
import os
from flask import Flask, render_template,redirect,request,url_for,session
import sqlite3


app=Flask(__name__)

UPLOAD_FOLDER="static/img/produtos"
app.config['UPLOAD_FOLDER']=  UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGHT']=16*1000*1000

app.secret_key="123"


@app.route('/')
def index():
  if "user" in session:
     con=sqlite3.connect('banco.db')
     cur=con.cursor()
     sql='select cep from usuario  where cpf=?'
     nome=session["user"]
     print(nome)
     cur.execute(sql,[nome])
     cep=cur.fetchall()
     cep=str(cep)
     cep=cep.replace("[","").replace("(", "").replace("]","").replace(")", "").replace("\'","").replace(",","")
     print(f'esse é o cep:{cep}')

    
     num='select numero from usuario where cpf=?'
     cur.execute(num,[nome])
     numero=cur.fetchall()
     numero=str(numero)
     numero=numero.replace("[","").replace("(", "").replace("]","").replace(")", "").replace("\'","").replace(",","")


   
     cep = cep.replace("-", "").replace(".", "").replace(" ", "")

     if len(cep) == 8:
      link = f"https://viacep.com.br/ws/{cep}/json/"
      requisicao = requests.get(link)
      dic_requisicao = requisicao.json()

      uf = dic_requisicao['uf']
      rua=dic_requisicao['logradouro']
      cidade = dic_requisicao['localidade']
      bairro = dic_requisicao['bairro']
      
      print(f"UF: {uf}, Cidade: {cidade}, Bairro: {bairro} rua: {rua}")
      selecionar='''
      select * from produtos 
      '''
      cur.execute(selecionar)
      con.commit()
      print(cur.fetchall())
      return render_template("consumidor/inicio.html", rua=rua, num=numero)
    
     else:
      print("CEP Inválido")
    
  

  return render_template('index.html')
@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/')
@app.route("/logoutComercio")
def logout_comerciante():
  session.pop('empresa')
  return redirect("/")
@app.route("/produto")
def mostrar():
  if "user" in session:
    return render_template('consumidor/p.html')

@app.route('/exibircadastro')
def exibirCadastro():
  return render_template('consumidor/cadastro.html')
@app.route('/cadastro', methods=['POST'])
def cadastro():
  con=sqlite3.connect('banco.db')
  cur=con.cursor()
  requisicao=request.form
  nome=requisicao['nome']
  cpf=requisicao['cpf']
  cep=requisicao['cep']
  numero=requisicao['numero']
  senha=requisicao['senha']
  sql="select cpf from usuario where cpf=?"
  cur.execute(sql,[cpf])
  ver=cur.fetchall()

  con.commit()
  if len(ver)>0:
    con.close()
    return redirect('/')

  sql='insert  into usuario (nome,cpf,senha,cep,numero) values(?,?,?,?,?)'
  session["user"]=cpf
  cur.execute(sql,[nome,cpf,senha,cep])
  con.commit()
  return redirect('/')
@app.route('/exibirLogin')
def exibirLogin():
  
  return render_template('consumidor/login.html')
@app.route('/login', methods=['POST'])
def login():
  con=sqlite3.connect('banco.db')
  cur=con.cursor()
  requisicao=request.form

  cpf=requisicao['cpf']
  senha=requisicao['senha']
  sql='select cpf,nome ,senha from usuario  where cpf=? and senha=?'
  
  cur.execute(sql,[cpf,senha])
  nomes=cur.fetchall()
  con.commit()
  nomes=str(nomes)
  nomes=nomes.replace("[","").replace("(", "").replace("]","").replace(")", "")
 
  print(nomes)
  
  if len(nomes)>0:
    print('ok')
    session["user"]=cpf
    
    return redirect('/')
  con.close
  return redirect('/exibirLogin')
@app.route('/comerciante')
def tela_inicial_comerciantes():
  if "empresa" in session:
      cnpj=session["empresa"]
      sql="select nome from comerciantes where cnpj=?"
      con=sqlite3.connect('banco.db')
      cur=con.cursor()
      cur.execute(sql,[cnpj])
      print(session['empresa'])
      cnpj=str(cnpj)
      cnpj=cnpj.replace("[","").replace("]","").replace("(","").replace(")","").replace(",","").replace("'","")
      
      
      
      con.commit()
      
      print(cnpj)
      
      sql='select nome,preco,img,descricao,id_l,id_p from produtos where id_l=?'
      cur.execute(sql,[cnpj])
      
      produtos=cur.fetchall()
      # print(produtos)
      # produtos=str(produtos)
      # produtos=produtos.replace("[","").replace("]","").replace("(","").replace(")","").replace("'","")
      # produtos=produtos.split(",")
      print(produtos)
      if len(produtos)>0:
        selecao_id='''
 select id from comerciantes where cnpj =? 
'''   
        cur.execute(selecao_id,[cnpj])
        con.commit()
        id=cur.fetchall()
        id=str(id).replace("[","").replace("]","").replace("(","").replace(")","").replace(",","").replace("'","")

         
       
 
        
        ordem=[]
        con.commit()
        for i in produtos:
           ordem.append(i)
           
      else:
        produtos="loja, sem produtos"
    
      
      
      return render_template('comerciante/comerciantes.html', id=id, ordem=ordem)
  else:
      return render_template('comerciante/comerciantes.html',id="")
@app.route('/cadastro_comerciantes')
def cadastrar_comerciantes():
  return render_template('comerciante/cadastroComerciante.html')
@app.route("/formulario_cadastro", methods=['post'])
def inserir():
  con=sqlite3.connect('banco.db')
  cur=con.cursor()
  requisicao=request.form
  nome=requisicao['nome']
  cnpj=requisicao['cnpj']
  cep=requisicao['cep']
  chave=requisicao['cep']
  senha=requisicao['senha']
  tipo=requisicao['tipo']
  numero=requisicao['numero']
  sql="select cnpj from comerciantes where cnpj=?"
  cur.execute(sql,[cnpj])
  
  con.commit()
  
  lista=cur.fetchall()
  if len(lista)>0:
    con.close()
    msg="ja cadastrado"
    return render_template('comerciante/loginComerciante.html')

  sql='insert  into comerciantes (nome,cnpj,cep,chave,senha,tipo,numero) values(?,?,?,?,?,?,?)'
  cur.execute(sql,[nome,cnpj,cep,chave,senha,tipo,numero])
  session["empresa"]=cnpj
  return redirect('/comerciante')


@app.route("/login_comerciante")
def  login_comerciante():
  print('ola')
  return render_template('comerciante/loginComerciante.html')


@app.route('/loginComerciante', methods=['POST'])
def loginComerciante():
  con=sqlite3.connect('banco.db')
  cur=con.cursor()
  requisicao=request.form

  cnpj=requisicao['cnpj']
  senha=requisicao['senha']
  sql='select cnpj,senha from comerciantes  where cnpj=? and senha=?'
  cnpj=str(cnpj).replace("'","")
  senha=str(senha).replace("'","")
  print(cnpj,senha)
  cur.execute(sql,[cnpj,senha])
  nomes=cur.fetchall()
  con.commit()
  nomes=str(nomes)
  nomes=nomes.replace("[","").replace("(", "").replace("]","").replace(")", "")
 
 
  print('tela login')
  if len(nomes)>0:
    print('ok')
    session["empresa"]=cnpj
    
    return redirect('/comerciante')
  else:        
    print('oque')
    con.close()
    return redirect('/login_comerciante')
@app.route("/inserir")
def mIN():
  if "empresa" in session:
    return render_template("comerciante/imagens.html")
  else:
    return render_template("comerciante/comerciantes.html")

@app.route("/mercados")
def produtos():
  if "user" in session:
      con=sqlite3.connect('banco.db')
      cur=con.cursor()
      restaurante="mercados"
      sql='select nome,cnpj,tipo,cep,id from comerciantes where tipo = ?'
      cur.execute(sql,[restaurante])
  
      lista=cur.fetchall()
     
      print(lista)
      
      ordem=[]
      con.commit()
      if len(lista)>0:
        
        for i in lista:
        
         ordem.append(i)
         con.close()
         return render_template('consumidor/mercados.html', ordem=ordem)
      else:
         return render_template("consumidor/mercados.html", ordem="")
    
       
@app.route("/restaurantes")

def restaurantes():
  if "user" in session:
      con=sqlite3.connect('banco.db')
      cur=con.cursor()
      restaurante="restaurante"
      sql='select nome,cnpj,tipo,cep,id from comerciantes where tipo = ?'
      cur.execute(sql,[restaurante])
  
      lista=cur.fetchall()
     
      print(lista)
      
      ordem=[]
      con.commit()
      j=0
      for i in lista:
        
        ordem.append(i)
        print(ordem[j])
        j+=1
      con.close()
      return render_template('consumidor/restaurantes.html', ordem=ordem)
@app.route("/loja<id>")
def exibir_loja(id):
  if "user" in session:
    con=sqlite3.connect('banco.db')
    cur=con.cursor()
    con.commit()
    select="select cnpj from comerciantes where id=?"
    cur.execute(select,[id])
    cnpj=cur.fetchall()
 

   
    if len(cnpj)>0:
      cnpj=str(cnpj)
      cnpj=cnpj.replace("[","").replace("]","").replace("(","").replace(")","").replace(",","").replace("'","")
      
      
      
      con.commit()
      
      print(cnpj)
      
      sql='select nome,preco,img,descricao,id_l,id_p from produtos where id_l=?'
      cur.execute(sql,[cnpj])
      
      produtos=cur.fetchall()
      # print(produtos)
      # produtos=str(produtos)
      # produtos=produtos.replace("[","").replace("]","").replace("(","").replace(")","").replace("'","")
      # produtos=produtos.split(",")
      print(produtos)
      if len(produtos)>0:
        
         
       
 
        
        ordem=[]
        con.commit()
        for i in produtos:
           ordem.append(i)
        print(ordem)
        return render_template("consumidor/lojas.html", produtos=ordem)
      else:
        produtos="loja, sem produtos"
        return produtos
  
        
  else:
    return redirect('/')
   
@app.route('/produtos', methods=['POST'])
def upload_file():
    if "empresa" in session:
      con=sqlite3.connect('banco.db')
      cur=con.cursor()
      reque=request.form
      nome=reque['nome']
      descricao=reque['descricao']
      preco=reque['preco']
      if 'produto' not in request.files:
          return 'Nenhum arquivo foi enviado.', 400
      
      file = request.files['produto']
      print(f'esse  o nome {file.filename}')
      if file.filename == '':
          return 'Nenhum arquivo selecionado para upload.', 400

      if file:
          filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
          file.save(filename)
          sql='''
          insert into produtos(nome,id_l,preco,img,descricao) values(?,?,?,?,?)
          '''
          cur.execute(sql,[nome,session["empresa"],preco,file.filename,descricao])
          con.commit()
          return 'Arquivo salvo com sucesso.', 200
@app.route("/comprar<id_p>")
def compras(id_p):
  if "user" in session:
    
    return render_template('consumidor/compras.html')
  else:
    redirect("/")
@app.route("/carrinho<id_p>")
def carrinho(id_p):
  if "user" in session:
    
    return render_template('consumidor/carrinho.html')
  else:
    redirect("/")
@app.route("/relatorio<id>")
def  relatorio(id):
  if "empresa" in session:
#     sql='''
# select quantidade,preco,produto from numero_vendas where id_m=?
# '''


    return render_template('comerciante/vendas.html')
@app.route("/bebidas")

def bebidas():
  if "user" in session:
      con=sqlite3.connect('banco.db')
      cur=con.cursor()
      restaurante="bebidas"
      sql='select nome,cnpj,tipo,cep,id from comerciantes where tipo = ?'
      cur.execute(sql,[restaurante])
  
      lista=cur.fetchall()
     
      print(lista)
      
      ordem=[]
      con.commit()
      j=0
      for i in lista:
        
        ordem.append(i)
        print(ordem[j])
        j+=1
      con.close()
      if len(ordem)>0:
        
        return render_template('consumidor/bebidas.html', ordem=ordem)
      else:
       return render_template('consumidor/bebidas.html', ordem="")
@app.route("/kitanda")

def kitanda():
  if "user" in session:
      con=sqlite3.connect('banco.db')
      cur=con.cursor()
      restaurante="kitanda"
      sql='select nome,cnpj,tipo,cep,id from comerciantes where tipo = ?'
      cur.execute(sql,[restaurante])
  
      lista=cur.fetchall()
     
      print(lista)
      
      ordem=[]
      con.commit()
      j=0
      for i in lista:
        
        ordem.append(i)
        print(ordem[j])
        j+=1
      con.close()
      if len(ordem)>0:
        
        return render_template('consumidor/kitanda.html', ordem=ordem)
      else:
       return render_template('consumidor/kitanda.html', ordem="")
    
@app.route("/drogaria")

def drogaria():
  if "user" in session:
      con=sqlite3.connect('banco.db')
      cur=con.cursor()
      restaurante="drogarias"
      sql='select nome,cnpj,tipo,cep,id from comerciantes where tipo = ?'
      cur.execute(sql,[restaurante])
  
      lista=cur.fetchall()
     
      print(lista)
      
      ordem=[]
      con.commit()
      j=0
      for i in lista:
        
        ordem.append(i)
        print(ordem[j])
        j+=1
      con.close()
      if len(ordem)>0:
        
        return render_template('consumidor/kitanda.html', ordem=ordem)
      else:
       return render_template('consumidor/kitanda.html', ordem="")

@app.route("/servicos")

def servicos():
  if "user" in session:
      con=sqlite3.connect('banco.db')
      cur=con.cursor()
      restaurante="kitanda"
      sql='select nome,cnpj,tipo,cep,id from comerciantes where tipo = ?'
      cur.execute(sql,[restaurante])
  
      lista=cur.fetchall()
     
      print(lista)
      
      ordem=[]
      con.commit()
      j=0
      for i in lista:
        
        ordem.append(i)
        print(ordem[j])
        j+=1
      con.close()
      if len(ordem)>0:
        
        return render_template('consumidor/servicos.html', ordem=ordem)
      else:
       return render_template('consumidor/servicos.html', ordem="")
@app.route("/carrinho/<id>")
def carrinho_inserir(id):
  if "user" in session:
    con=sqlite3.connect('banco.db')
    cur=con.cursor()
    print('allysson')
    print(id)
    selecao='''
  select id_l,nome,preco,img, descricao from produtos where id_p=?
'''
    cur.execute(selecao,[id])
    resultados=cur.fetchall()
    con.commit()
    print(resultados)
    print('teste')
    if len(resultados)>0:
      resultados=str(resultados).replace("[","").replace("]","").replace("(","").replace(")","").replace(",","").replace("'","")
      
      resultados=resultados.split()
      cnpj=resultados[0]
      nome=resultados[1]
      preco=resultados[2]
      nome_arquivo=resultados[3]+resultados[4]
      descricao=resultados[5]+resultados[6]
      print(nome_arquivo)
      print(f' toda a lista{resultados}')
      print(f'esse é o {cnpj}')
      sql='''
insert into carrinho(nome,id_l,id_p,preco,img,descricao) values(?,?,?,?,?,?)
'''
    cur.execute(sql,[])
    con.commit()

    print('fez')
    return render_template("consumidor/carrinho.html",ordem='teste')
@app.route('/exibirMoto')
def exibirMoto():
  return render_template('motoboy/cadastro.html')
@app.route('/cadastroMoto', methods=['POST'])
def cadastroMoto():
  con=sqlite3.connect('banco.db')
  cur=con.cursor()
  requisicao=request.form
  nome=requisicao['nome']
  cpf=requisicao['cpf']
  cep=requisicao['cep']
  senha=requisicao['senha']
  sql="select cpf from motoboy where cpf=?"
  cur.execute(sql,[cpf])
  ver=cur.fetchall()
  print(cep)
  con.commit()
  if len(ver)>0:
    con.close()
    return redirect('/')

  sql='insert  into motoboy (nome,cpf,senha,cep) values(?,?,?,?,?)'
  session["motoboy"]=cpf
  cur.execute(sql,[nome,cpf,senha,cep])
  con.commit()
  return render_template('motoboy/entrega.html')
@app.route('/exibirMotoboy')
def exibirMotoboy():
  
  return render_template('motoboy/login.html')
@app.route('/loginMoto', methods=['POST'])
def loginMoto():
  con=sqlite3.connect('banco.db')
  cur=con.cursor()
  requisicao=request.form

  cpf=requisicao['cpf']
  senha=requisicao['senha']
  sql='select cpf,nome ,senha from motoboy where cpf=? and senha=?'
  
  cur.execute(sql,[cpf,senha])
  nomes=cur.fetchall()
  con.commit()
  nomes=str(nomes)
  nomes=nomes.replace("[","").replace("(", "").replace("]","").replace(")", "")
 
  print(nomes)
  
  if len(nomes)>0:
    print('ok')
    session["motoboy"]=cpf
    
    return render_template('motoboy/entrega.html')
app.run(host='0.0.0.0', port=85, debug=True)