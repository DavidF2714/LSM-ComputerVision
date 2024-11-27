import Image from 'next/image'

import TestimonialImage01 from '@/public/images/testimonial-01.jpg'
import TestimonialImage02 from '@/public/images/testimonial-02.jpg'
import TestimonialImage03 from '@/public/images/testimonial-03.jpg'

export default function Overview() {
  return (
    <section id = "Overview">
      <div className="max-w-6xl mx-auto px-4 sm:px-6">
        <div className="py-12 md:py-20 border-t border-gray-800">

          {/* Section header */}
          <div className="max-w-3xl mx-auto text-center pb-12 md:pb-20">
            <h2 className="h2 mb-4">Lengua de Señas Mexicana: Su importancia e información clave.</h2>
            <p className="text-xl text-gray-400"> Aprenda más sobre la Lengua de Señas Mexicana, su papel en la inclusión y explore su diccionario.</p>
          </div>

          {/* Testimonials */}
          <div className="max-w-sm mx-auto grid gap-8 lg:grid-cols-3 lg:gap-6 items-start lg:max-w-none">

            {/* 1st testimonial */}
            <div className="flex flex-col h-full p-6 bg-gray-800" data-aos="fade-up">
             
              <h5 className="h4 mb-2 m-auto">¿Qué es la Lengua de Señas Mexicana?</h5>

              <hr className="border-t-1 border-gray-700 my-5" />
              
              <p className="text-lg text-gray-400 text-center">La Lengua de Señas Mexicana (LSM) es la lengua mayoritaria de la comunidad sorda de México reconocida en 2011 como una lengua nacional oficial y que tiene cerca de 300,000 hablantes en todo el país. consiste en una serie de signos gestuales articulados con las manos y acompañados de expresiones faciales, mirada intencional y movimiento corporal, dotados de función lingüística.</p>
              
              <div className="text-gray-700 font-medium mt-6 pt-5 border-t border-gray-700">

                <a className="text-purple-600 hover:text-gray-200 transition duration-150 ease-in-out" href="https://www.gob.mx/conadis/articulos/lengua-de-senas-mexicana-lsm">Aprende más sobre la Lengua de Señas Mexicana</a>
              </div>
            </div>

            {/* 2nd testimonial */}

            <div className="flex flex-col h-full p-6 bg-gray-800" data-aos="fade-up">
             
              <h5 className="h4 mb-2 m-auto">Importancia de la LSM</h5>

              <hr className="border-t-1 border-gray-700 my-5" />

              <p className="text-lg text-gray-400 text-center"> La importancia de la Lengua de Señas Mexicana reside en la dificultad de las personas con discapacidad auditiva para comunicarse con los demás, lo que puede dificultar su desarrollo en distintos ámbitos y limitar sus oportunidades. Actualmente la Lengua de Señas Mexicana es la lengua en la que las personas que han nacido sordos o han quedado sordos expresan sus pensamientos y emociones, lo que satisface sus necesidades comunicativas y permite el desarrollo de sus capacidades cognitivas.</p>
              
              <div className="text-gray-700 font-medium mt-6 pt-5 border-t border-gray-700">

                <a className="text-purple-600 hover:text-gray-200 transition duration-150 ease-in-out" href="https://www.cndh.org.mx/noticia/dia-nacional-de-la-lengua-de-senas-mexicana-10-de-junio-0">Lee acerca del dia nacional de la LSM</a>
              </div>
            </div>

            {/* 3rd testimonial */}
            <div className="flex flex-col h-full p-6 bg-gray-800" data-aos="fade-up">
             
              <h5 className="h4 mb-2 m-auto">Aprende Lengua de Señas Mexicana</h5>

              <hr className="border-t-1 border-gray-700 my-5" />

              <p className="text-lg text-gray-400 text-center">El conocer y aprender a hablar LSM es de vital importancia para la inclusión de las personas pertenecientes a la comunidad sorda, además de ayudar a reconocer la riqueza cultural y lingüística de esta comunidad, contribuyendo a su integración y valoración en la sociedad.
              Conocer y aprender sobre este tema también contribuye a crear conciencia sobre los desafíos que enfrentan las personas sordas y cómo solucionarlos. Écha un vistazo al diccionario de la LSM y aprende más sobre su gramática y léxico</p>
              
              <div className="text-gray-700 font-medium mt-6 pt-5 border-t border-gray-700">

                <a className="text-purple-600 hover:text-gray-200 transition duration-150 ease-in-out" href="https://educacionespecial.sep.gob.mx/storage/recursos/2023/05/xzrfl019nV-4Diccionario_lengua_%20Senas.pdf">Diccionario de la LSM</a>
              </div>
            </div>

           

           

          </div>

        </div>
      </div>
    </section>
  )
}
