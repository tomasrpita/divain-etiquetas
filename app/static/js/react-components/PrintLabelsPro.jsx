import { useFetch2 as useFetch } from "./hooks/useFetch2"

// TODO: move to a config file
const codestMap = {
    "MEX": "MX",
    "USA": "USA",
    "ESP": "UE",
    "UK": "UK"
}

const getEtiquetaFields = (category, sex) => {
    const etiquetaField = {
        value: ''
    };

    console.log({ category, sex });

    if (category == 'divain') {


        // Misma impresión Solo NUmeros Centrados
        // file: syandard_100ml
        // ETIQUETA Standard Femme
        // 8436592101047
        if (sex == 'F E M M E') {
            etiquetaField.value = 'ESTANDAR - FEMME';
            // ETIQUETA Standard Homme
            // 8436596740037
        } else if (sex == 'H O M M E') {
            etiquetaField.value = 'ESTANDAR - HOMME';
            // ETIQUETA Standard Unisex
            //8436596741287
        } else if (sex == 'U N I S E X') {
            etiquetaField.value = 'ESTANDAR - UNISEX';


            // ETIQUETA kids
            // Una Sola Etiqueta
            // debe imprimir: número, raya, sex y lote (centrado).
            // file: xHacer
            // 8436592109036
        }
        else if (sex == 'K I D S') {
            etiquetaField.value = 'KIDS';

        }


        // Una etiqueta que puede ser BLACK_EDITION_HOMME, BLACK_EDITION_FEMME, BLACK_EDITION_UNISEX
        // debe imprimir: número, raya y sex (centrado).
        // file: xHacer
        // 8436592102969
    } else if (category == 'black') {
        etiquetaField.value = 'BLACK EDITION';

        // ETIQUETA SOLIDARIO_UNISEX
        // Debe imprimir: número, raya y sex (centrado).
        // file: xHacer
        // 8436592109937
    } else if (category == 'solidario') {
        etiquetaField.value = 'SOLIDARIO UNISEX';

    }

    return etiquetaField;
}

export const PrintLabelsPro = () => {

    const [codeInput, setCodeInput] = React.useState('');
    const [error, setError] = React.useState('');
    const [drawer, setDrawer] = React.useState('');
    const [sku, setSKU] = React.useState('');
    const [ean13s, setEan13s] = React.useState([]);
    const [ean128s, setEan128s] = React.useState([]);
    const [bottles, setBottles] = React.useState(0);
    const [bottlesChecked, setBottlesChecked] = React.useState(0);
    const [productionOrderId, setProductionOrderId] = React.useState(0);
    const [ean13Ean128Map, setean13Ean128Map] = React.useState({});
    const [batch, setBatch] = React.useState('');
    const [etiquetaField, setEtiquetaField] = React.useState({
        value: ''
    });
    const [labelDestination, setLabelDestination] = React.useState('UE');
    const [codest, setCodest] = React.useState('');


    const iptControl = React.useRef();
    const [{ data, isLoading, hasError }, setFetchUrl, setFetchMethod, setFetchBody] = useFetch();

    React.useEffect(() => {
        iptControl.current.focus();
    }, []);

    React.useEffect(() => {
        if (data && data.production_order_id) {
            setDrawer(codeInput);
            // setLocation(data.location_name);
            iptControl.current.setAttribute('placeholder', 'Ingrese EAN128 de la botella');
            // setEan13(data.ean13_list[0]);
            // setIsBlocked(true);
            // setBottles(data.ean13_list.length);
            setProductionOrderId(data.production_order_id);
            setSKU(data.divain_sku);
            setEan13s(data.ean13_list);
            setBottles(data.ean13_list.length);
            setBatch(data.batch);
            setCodest(data.codest_name);
            setDrawer(codeInput);
            setLabelDestination(codestMap[data.codest_name]);

            // Se dan casos que no la reucpera por ean13
            // corregir como se cargan los datos, tal vez solo 
            // trae los ean13 por proveedor por omisión
            const ean13 = data.ean13_list[0];
            const divain_number = data.divain_sku.split('-')[1];
            const labelInfo = findLabelInfo(ean13) || findLabelInfo(divain_number);
            if (labelInfo) {
                // TODO: traer toda la data de la etiqueta de una vez
                setEtiquetaField(getEtiquetaFields(labelInfo.category, labelInfo.sex));
            }
            setCodeInput('');
            audioPlay('success');
            iptControl.current.focus();


        }

    }, [data]);

    React.useEffect(() => {
        // Es la cantidad de etiquetas a imprimir luego de haberles creado el ean128
        if (data && data.labels_to_print) {
            // const labelInfo = findLabelInfo(sku);
            const ean13 = Object.keys(ean13Ean128Map)[0];
            const divain_number = sku.split('-')[1];
            const labelInfo = findLabelInfo(ean13) || findLabelInfo(divain_number);

            if (labelInfo) {
                console.log({ labelInfo });
                const labelInfoToPrint = {
                    "CopiesNumber": data.labels_to_print,
                    "tscLabel": 'bottle',
                    "zdLabel": 'destination_group',
                    "label_destination": labelDestination,
                    "eanBotella": labelInfo.supplier_references_eans[0],
                    "loteBotella": batch,
                    "ean_botes": labelInfo.ean_bottle,
                    "ean_muestras": labelInfo.ean_sample,
                    "numero_divain": labelInfo.divain_number,
                    "sexo": labelInfo.sex,
                    "sku": labelInfo.sku_divain,
                    "categoria": labelInfo.category,
                    "ingredientes": labelInfo.ingredients,
                    "fragance_name": labelInfo.fragance_name
                };

                setFetchMethod('POST');
                setFetchBody(labelInfoToPrint);
                setFetchUrl('/pro/print');


            } else {
                setError('No se encontró información de la etiqueta');
                iptControl.current.classList.add("is-invalid");
                setTimeout(() => {
                    audioPlay('wrong');
                }, 300);
                return;
            }
            iptControl.current.focus();

        }
    }, [data]);

    React.useEffect(() => {

        if (data && data.printed) {
            console.log({ data });
            window.location.href = '/pro';

        }

    }, [data]);




    React.useEffect(() => {
        console.log({ bottlesChecked });
        // Select all bottle icons
        const bottleIcons = document.querySelectorAll('.fa-wine-bottle');

        // Update the class of the bottle icons based on bottlesChecked
        bottleIcons.forEach((icon, index) => {
            if (index < bottlesChecked) {
                icon.classList.remove('text-muted');
                icon.classList.add('text-success');
            } else {
                icon.classList.add('text-muted');
                icon.classList.remove('text-success');
            }
        });
    }, [bottlesChecked]);


    React.useEffect(() => {
        if (hasError || error) {
            setTimeout(() => {
                audioPlay('wrong');
            }, 300);
            setCodeInput('');
            iptControl.current.focus();
        }
    }, [hasError, error]);


    const handleInputChange = (e) => {
        // to upper case
        const newValue = e.target.value.toUpperCase();
        setCodeInput(newValue);
    }

    const handleKeyDown = (e) => {
        if (e.key === 'Enter') {
            console.log("Enter");
            setError('');
            iptControl.current.classList.remove("is-invalid");

            if (!e.target.value) {
                return;
            }

            audioPlay('beep');

            if (!drawer) {
                console.log({ codeInput });
                setFetchUrl(apiProductionOrder + codeInput);

            } else if (drawer && bottlesChecked < bottles) {
                const ean128 = codeInput;
                const currentBottle = ean13s.find(ean13 => ean13 === getEan13(ean128));
                console.log({ currentBottle });
                if (currentBottle) {
                    setEan128s([...ean128s, ean128]);
                    // extract ean13 from eans13 list
                    const index = ean13s.findIndex(ean13 => ean13 === currentBottle);
                    if (index !== -1) {
                        ean13s.splice(index, 1);
                    }
                    setEan13s([...ean13s]);
                    // create this maps type:
                    // "ean13_ean128_dict": {
                    //     "8423564090133": ["(01)8423564090133(17)231231(10)BATCH1234", "(01)8423564090133(17)231231(10)BATCH4321"]
                    //     }
                    const currentEan13Ean128Array = ean13Ean128Map[currentBottle] || [];
                    currentEan13Ean128Array.push(ean128);
                    ean13Ean128Map[currentBottle] = currentEan13Ean128Array;
                    setean13Ean128Map(ean13Ean128Map);

                    setBottlesChecked(bottlesChecked + 1);
                    setCodeInput('');
                    // audioPlay('success');
                    // console.log({ ean13Ean128Map });
                    // console.log({ bottlesChecked });
                    // console.log({ bottles });
                    if (bottlesChecked + 1 === bottles) {
                        iptControl.current.setAttribute('placeholder', 'Confirme gaveta para imprimir etiquetas ');
                    }
                } else {
                    setError('EAN128 incorrecto');
                    iptControl.current.classList.add("is-invalid");
                }
            } else if (drawer && bottlesChecked === bottles) {

                console.log({ ean13Ean128Map });
                if (codeInput !== drawer) {
                    setError('Gaveta incorrecta');
                    iptControl.current.classList.add("is-invalid");
                }


                // const ean13Ean128Dict = JSON.stringify(ean13Ean128Map);
                // const body = { ean13_ean128_dict: ean13Ean128Dict };
                const body = { production_order_id: productionOrderId, ean13_ean128_dict: ean13Ean128Map };
                setFetchBody(body);
                setFetchMethod('POST');
                setFetchUrl(apiProductionOrder);
            }

        }
    }

    return (
        <>
            <div className="form-group row">
                <div className="col-3">
                    <label className="col-form-label">Introduzca:</label>
                </div>
                <div className="col-7">
                    <input type="text"
                        ref={iptControl}
                        className="form-control"
                        placeholder="Ingrese ID de la Gaveta"
                        value={codeInput}
                        onChange={handleInputChange}
                        onKeyDown={handleKeyDown}
                    />
                    {error &&
                        <small id="smallControl" className="form-text text-danger ">{error}</small>
                    }
                </div>

                <div id="spinnerControl" className="col-2 ">
                    {isLoading &&
                        <div className="spinner-border text-warning" role="status">
                            <span className="sr-only">Loading...</span>
                        </div>
                    }
                </div>
            </div>
            <div className="form-group row">
                <div className="col-3">
                    <label className="col-form-label">Tipo Etiquetas destino:</label>
                </div>
                <div className="col-7">
                    <div className="form-check form-check-inline">
                        <input className="form-check-input" type="radio" name="labelDestination" id="ue" value="UE" checked={labelDestination === 'UE'} onChange={(e) => setLabelDestination(e.target.value)} />
                        <label className="form-check-label" htmlFor="ue">UE</label>
                    </div>
                    <div className="form-check form-check-inline">
                        <input className="form-check-input" type="radio" name="labelDestination" id="uk" value="UK" checked={labelDestination === 'UK'} onChange={(e) => setLabelDestination(e.target.value)} />
                        <label className="form-check-label" htmlFor="uk">UK</label>
                    </div>
                    <div className="form-check form-check-inline">
                        <input className="form-check-input" type="radio" name="labelDestination" id="usa" value="USA" checked={labelDestination === 'USA'} onChange={(e) => setLabelDestination(e.target.value)} />
                        <label className="form-check-label" htmlFor="usa">USA</label>
                    </div>
                    <div className="form-check form-check-inline">
                        <input className="form-check-input" type="radio" name="labelDestination" id="mx" value="MX" checked={labelDestination === 'MX'} onChange={(e) => setLabelDestination(e.target.value)} />
                        <label className="form-check-label" htmlFor="mx">MX</label>
                    </div>
                </div>
            </div>
            <div className="form-group row">
                <div className="col-3">
                    <label className="col-form-label">Gaveta:</label>
                </div>
                <div className="col-7">
                    <input type="text" className="form-control" value={drawer} readOnly />
                </div>
            </div>
            <div className="form-group row">
                <div className="col-3">
                    <label className="col-form-label">CODEST:</label>
                </div>
                <div className="col-7">
                    <input type="text" className="form-control" value={codest} readOnly />
                </div>
            </div>
            <div className="form-group row">
                <div className="col-3">
                    <label className="col-form-label">Lote:</label>
                </div>
                <div className="col-7">
                    <input type="text" className="form-control" value={batch} readOnly />
                </div>
            </div>
            <div className="form-group row">
                <div className="col-3">
                    <label className="col-form-label">SKU:</label>
                </div>
                <div className="col-7">
                    <input type="text" className="form-control" value={sku} readOnly />
                </div>
            </div>
            <div className="form-group row">
                <div className="col-3">
                    <label className="col-form-label">etiqueta:</label>
                </div>
                <div className="col-7">
                    <input type="text" className="form-control" value={etiquetaField.value} readOnly />
                </div>
            </div>
            <div className="form-group row">
                <div className="col-3">
                    <label className="col-form-label">
                        EANs13:
                    </label>
                </div>
                <div className="col-7">
                    <textarea className="form-control" rows="3" value={ean13s.join(', ')} readOnly></textarea>
                </div>
            </div>
            <div className="form-group row">
                <div className="col-3">
                    <label className="col-form-label">
                        EANs128:
                    </label>
                </div>
                <div className="col-7">
                    <textarea className="form-control" rows="4" value={ean128s.join(', ')} readOnly></textarea>
                </div>
            </div>
            <div className="form-group row">
                <div className="col-3">
                    <label className="col-form-label">Van:</label>
                </div>
                <div className="col-7">
                    {
                        !bottles &&
                        <span className="text-muted"><i className="fas fa-wine-bottle"></i></span>
                    }
                    {
                        Array.from({ length: bottles }).map((_, i) =>
                            <span key={i} className="text-muted"><i className="fas fa-wine-bottle"></i></span>
                        )
                    }

                </div>
            </div>

            {hasError &&
                <div className="alert alert-danger alert-dismissible fade show" role="alert">
                    <strong>¡ERROR!</strong> {hasError}
                    {/* <button type="button" className="close btn-close" data-dismiss="alert" data-bs-dismiss="alert" aria-label="Cerrar">
                        <span aria-hidden="true">&times;</span>
                    </button> */}
                </div>
            }
        </>
    )
}
