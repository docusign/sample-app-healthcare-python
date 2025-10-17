from datetime import datetime
from typing import Optional
from docusign_esign import Signer, Checkbox, Text, TabGroup, Number, Tabs, SignHere, DateSigned, SignerAttachment
from docusign.extensions import Extensions

def make_tabs_with_extensions(session):
    extensions = Extensions.get_extension_apps(session)
    phone_extension = Extensions.get_extension_by_app_id(extensions, Extensions.get_phone_extension_id())
    address_extension = Extensions.get_extension_by_app_id(extensions, Extensions.get_address_extension_id())
    ssn_extension = Extensions.get_extension_by_app_id(extensions, Extensions.get_ssn_extension_id())

    # define phone tab
    for tab in (t for t in phone_extension["tabs"] if "VerifyPhoneNumberInput[0].phoneNumber" in t["tabLabel"]):
        verification_data = Extensions.extract_verification_data(phone_extension["appId"], tab)
        extension_data = Extensions.get_extension_data(verification_data)
        phone = Text(
            name = verification_data["application_name"],
            tab_label = verification_data["tab_label"],
            tooltip = verification_data["action_input_key"],
            document_id = '1',
            page_number = '1',
            anchor_string = '/phone/',
            anchor_units = 'pixels',
            required = True,
            locked = False,
            anchor_y_offset = '-5',
            width = "120",
            extension_data = extension_data
        )

    # define address tabs
    address_fields = {
        "address": "VerifyPostalAddressInput[0].street1",
        "country": "VerifyPostalAddressInput[0].countryOrRegion",
        "state": "VerifyPostalAddressInput[0].subdivision",
        "city": "VerifyPostalAddressInput[0].locality",
        "zip": "VerifyPostalAddressInput[0].postalCode",
    }
    address_fields_width = {
        "address": "150",
        "country": "120",
        "state": "30",
        "city": "150",
        "zip": "60",
    }
    address_tabs = []
    for field, label_pattern in address_fields.items():
        for tab in (t for t in address_extension["tabs"] if label_pattern in t["tabLabel"]):
            verification_data = Extensions.extract_verification_data(address_extension["appId"], tab)
            extension_data = Extensions.get_extension_data(verification_data)
            address_tabs.append(Text(
                    name = verification_data["application_name"],
                    tab_label = verification_data["tab_label"],
                    tooltip = verification_data["action_input_key"],
                    document_id = "1",
                    page_number = "1",
                    anchor_string = f"/{field}/",
                    anchor_units = "pixels",
                    anchor_y_offset = '-5',
                    required = True,
                    locked = False,
                    width = address_fields_width[field],
                    extension_data = extension_data,
                )
            )

    # define SSN tab
    for tab in (t for t in ssn_extension["tabs"] if "VerifySocialSecurityNumberInput[0].socialSecurityNumber" in t["tabLabel"]):
        verification_data = Extensions.extract_verification_data(ssn_extension["appId"], tab)
        extension_data = Extensions.get_extension_data(verification_data)
        ssn = Text(
            name = verification_data["application_name"],
            tab_label = verification_data["tab_label"],
            tooltip = verification_data["action_input_key"],
            document_id = '1',
            page_number = '1',
            anchor_string = '/ssn/',
            anchor_units = 'pixels',
            required = True,
            locked = False,
            anchor_y_offset = '-5',
            extension_data = extension_data
        )

    return phone, address_tabs, ssn

def make_tabs_without_extensions():
    ssn = Text(
        document_id="1", page_number="1", anchor_string='/ssn/', anchor_units='pixels',
        required="true", tab_label="ssn", height="12", width="150", anchor_y_offset= "-5",
        validation_message="SSN format: xxx-xx-xxxx",
        validation_pattern="^[0-9]{3}-[0-9]{2}-[0-9]{4}$"
    )

    address_tabs = []
    address_tabs.append(Text(
        document_id="1", page_number="1", anchor_string="/address/", anchor_units="pixels",
        required="true", tab_label="address", height="12", width="150", anchor_y_offset= "-5"
    ))
    address_tabs.append(Text(
        document_id="1", page_number="1", anchor_string="/country/", anchor_units="pixels",
        required="true", tab_label="country", height="12", width="120", anchor_y_offset= "-5"
    ))
    address_tabs.append(Text(
        document_id="1", page_number="1", anchor_string="/city/", anchor_units="pixels",
        required="true", tab_label="city", height="12", width="150", anchor_y_offset= "-5"
    ))
    address_tabs.append(Text(
        document_id="1", page_number="1", anchor_string="/state/", anchor_units="pixels",
        required="true", tab_label="state", height="12", width="30", anchor_y_offset= "-5"
    ))
    address_tabs.append(Text(
        document_id="1", page_number="1", anchor_string="/zip/", anchor_units="pixels",
        required="true", tab_label="zip", height="12", width="60", anchor_y_offset= "-5"
    ))

    phone = Number(
        document_id="1", page_number="1", anchor_string="/phone/", anchor_units="pixels",
        required="true", tab_label="phone1", height="12", width="150", anchor_y_offset= "-5"
    )

    return phone, address_tabs, ssn

def make_application_for_participation_signer(args, session):
    """
    Create signer and fields using absolute positioning
    Add the tabs model to the signer
    """

    # Create the signer recipient model
    signer = Signer(
        role_name="signer",
        recipient_id="1",
        routing_order="1"
    )

    # Create fields
    first_name = Text(
        document_id="1", page_number="1", x_position="45", y_position="168",
        required="true", tab_label="first_name", height="12", width="60"
    )
    last_name = Text(
        document_id="1", page_number="1", x_position="231", y_position="168",
        required="true", tab_label="last_name", height="12", width="60"
    )

    family_size = Number(
        document_id="1", page_number="1", x_position="399", y_position="252",
        required="true", tab_label="family_size", height="12", width="30"
    )

    check1 = Checkbox(
        document_id="1", page_number="1", tab_label="check1",
        tab_group_labels=["yn0"], required="false", x_position="477", y_position="255",
    )
    check2 = Checkbox(
        document_id="1", page_number="1", tab_label="check2",
        tab_group_labels=["yn0"], required="false", x_position="530", y_position="255",
    )
    yn0 = TabGroup(
        document_id="1", page_number="1", recipient_id="1", tab_scope="Document",
        group_rule="SelectExactly", minimum_required="1", maximum_allowed="1",
        group_label="yn0"
    )

    individual_assets = Text(
        document_id="1", page_number="1", x_position="399", y_position="313",
        required="false", tab_label="individual_assets", height="12", width="60"
    )
    family_assets = Text(
        document_id="1", page_number="1", x_position="399", y_position="337",
        required="false", tab_label="family_assets", height="12", width="60"
    )
    asset1 = Text(
        document_id="1", page_number="1", x_position="399", y_position="385",
        required="false", tab_label="asset1", height="12", width="60"
    )
    asset2 = Text(
        document_id="1", page_number="1", x_position="399", y_position="409",
        required="false", tab_label="asset2", height="12", width="60"
    )
    asset3 = Text(
        document_id="1", page_number="1", x_position="399", y_position="433",
        required="false", tab_label="asset3", height="12", width="60"
    )
    asset4 = Text(
        document_id="1", page_number="1", x_position="399", y_position="457",
        required="false", tab_label="asset4", height="12", width="60"
    )
    asset5 = Text(
        document_id="1", page_number="1", x_position="399", y_position="481",
        required="false", tab_label="asset5", height="12", width="60"
    )
    asset6 = Text(
        document_id="1", page_number="1", x_position="399", y_position="505",
        required="false", tab_label="asset6", height="12", width="60"
    )
    asset_total = Text(
        document_id="1", page_number="1", x_position="399", y_position="529",
        required="false", tab_label="asset_total", height="12", width="60"
    )

    income1 = Text(
      document_id="1", page_number="2", x_position="281", y_position="92",
      required="false", tab_label="income1", height="12", width="60"
    )
    check3 = Checkbox(
        document_id="1", page_number="2", tab_label="check3",
        tab_group_labels=["yn1"], required="false", x_position="443", y_position="93",
    )
    check4 = Checkbox(
        document_id="1", page_number="2", tab_label="check4",
        tab_group_labels=["yn1"], required="false", x_position="494", y_position="93",
    )
    check5 = Checkbox(
        document_id="1", page_number="2", tab_label="check5",
        tab_group_labels=["yn1"], required="false", x_position="544", y_position="93",
    )
    yn1 = TabGroup(
        document_id="1", page_number="2", recipient_id="1", tab_scope="Document",
        group_rule="SelectAtMost", minimum_required="0", maximum_allowed="1",
        group_label="yn1"
    )

    income2 = Text(
      document_id="1", page_number="2", x_position="281", y_position="116",
      required="false", tab_label="income2", height="12", width="60"
    )
    check6 = Checkbox(
        document_id="1", page_number="2", tab_label="check6",
        tab_group_labels=["yn2"], required="false", x_position="443", y_position="118",
    )
    check7 = Checkbox(
        document_id="1", page_number="2", tab_label="check7",
        tab_group_labels=["yn2"], required="false", x_position="494", y_position="118",
    )
    check8 = Checkbox(
        document_id="1", page_number="2", tab_label="check8",
        tab_group_labels=["yn2"], required="false", x_position="544", y_position="118",
    )
    yn2 = TabGroup(
        document_id="1", page_number="2", recipient_id="1", tab_scope="Document",
        group_rule="SelectAtMost", minimum_required="0", maximum_allowed="1",
        group_label="yn2"
    )

    income3 = Text(
      document_id="1", page_number="2", x_position="281", y_position="140",
      required="false", tab_label="income3", height="12", width="60"
    )
    check9 = Checkbox(
        document_id="1", page_number="2", tab_label="check9",
        tab_group_labels=["yn3"], required="false", x_position="443", y_position="140",
    )
    check10 = Checkbox(
        document_id="1", page_number="2", tab_label="check10",
        tab_group_labels=["yn3"], required="false", x_position="494", y_position="140",
    )
    check11 = Checkbox(
        document_id="1", page_number="2", tab_label="check11",
        tab_group_labels=["yn3"], required="false", x_position="544", y_position="140",
    )
    yn3 = TabGroup(
        document_id="1", page_number="2", recipient_id="1", tab_scope="Document",
        group_rule="SelectAtMost", minimum_required="0", maximum_allowed="1",
        group_label="yn3"
    )

    income4 = Text(
      document_id="1", page_number="2", x_position="281", y_position="166",
      required="false", tab_label="income4", height="12", width="60"
    )
    check12 = Checkbox(
        document_id="1", page_number="2", tab_label="check12",
        tab_group_labels=["yn4"], required="false", x_position="443", y_position="166",
    )
    check13 = Checkbox(
        document_id="1", page_number="2", tab_label="check13",
        tab_group_labels=["yn4"], required="false", x_position="494", y_position="166",
    )
    check14 = Checkbox(
        document_id="1", page_number="2", tab_label="check14",
        tab_group_labels=["yn4"], required="false", x_position="544", y_position="166",
    )
    yn4 = TabGroup(
        document_id="1", page_number="2", recipient_id="1", tab_scope="Document",
        group_rule="SelectAtMost", minimum_required="0", maximum_allowed="1",
        group_label="yn4"
    )

    income5 = Text(
      document_id="1", page_number="2", x_position="281", y_position="190",
      required="false", tab_label="income5", height="12", width="60"
    )
    check15 = Checkbox(
        document_id="1", page_number="2", tab_label="check15",
        tab_group_labels=["yn5"], required="false", x_position="443", y_position="190",
    )
    check16 = Checkbox(
        document_id="1", page_number="2", tab_label="check16",
        tab_group_labels=["yn5"], required="false", x_position="494", y_position="190",
    )
    check17 = Checkbox(
        document_id="1", page_number="2", tab_label="check17",
        tab_group_labels=["yn5"], required="false", x_position="544", y_position="190",
    )
    yn5 = TabGroup(
        document_id="1", page_number="2", recipient_id="1", tab_scope="Document",
        group_rule="SelectAtMost", minimum_required="0", maximum_allowed="1",
        group_label="yn5"
    )

    income6 = Text(
      document_id="1", page_number="2", x_position="281", y_position="213",
      required="false", tab_label="income6", height="12", width="60"
    )
    check18 = Checkbox(
        document_id="1", page_number="2", tab_label="check18",
        tab_group_labels=["yn6"], required="false", x_position="443", y_position="213",
    )
    check19 = Checkbox(
        document_id="1", page_number="2", tab_label="check19",
        tab_group_labels=["yn6"], required="false", x_position="494", y_position="213",
    )
    check20 = Checkbox(
        document_id="1", page_number="2", tab_label="check20",
        tab_group_labels=["yn6"], required="false", x_position="544", y_position="213",
    )
    yn6 = TabGroup(
        document_id="1", page_number="2", recipient_id="1", tab_scope="Document",
        group_rule="SelectAtMost", minimum_required="0", maximum_allowed="1",
        group_label="yn6"
    )

    income7 = Text(
      document_id="1", page_number="2", x_position="281", y_position="237",
      required="false", tab_label="income7", height="12", width="60"
    )
    check21 = Checkbox(
        document_id="1", page_number="2", tab_label="check21",
        tab_group_labels=["yn7"], required="false", x_position="443", y_position="237",
    )
    check22 = Checkbox(
        document_id="1", page_number="2", tab_label="check22",
        tab_group_labels=["yn7"], required="false", x_position="494", y_position="237",
    )
    check23 = Checkbox(
        document_id="1", page_number="2", tab_label="check23",
        tab_group_labels=["yn7"], required="false", x_position="544", y_position="237",
    )
    yn7 = TabGroup(
        document_id="1", page_number="2", recipient_id="1", tab_scope="Document",
        group_rule="SelectAtMost", minimum_required="0", maximum_allowed="1",
        group_label="yn7"
    )

    income8 = Text(
      document_id="1", page_number="2", x_position="281", y_position="261",
      required="false", tab_label="income8", height="12", width="60"
    )
    check24 = Checkbox(
        document_id="1", page_number="2", tab_label="check24",
        tab_group_labels=["yn8"], required="false", x_position="443", y_position="261",
    )
    check25 = Checkbox(
        document_id="1", page_number="2", tab_label="check25",
        tab_group_labels=["yn8"], required="false", x_position="494", y_position="261",
    )
    check26 = Checkbox(
        document_id="1", page_number="2", tab_label="check26",
        tab_group_labels=["yn8"], required="false", x_position="544", y_position="261",
    )
    yn8 = TabGroup(
        document_id="1", page_number="2", recipient_id="1", tab_scope="Document",
        group_rule="SelectAtMost", minimum_required="0", maximum_allowed="1",
        group_label="yn8"
    )

    income9 = Text(
      document_id="1", page_number="2", x_position="281", y_position="285",
      required="false", tab_label="income9", height="12", width="60"
    )
    check27 = Checkbox(
        document_id="1", page_number="2", tab_label="check27",
        tab_group_labels=["yn9"], required="false", x_position="443", y_position="285",
    )
    check28 = Checkbox(
        document_id="1", page_number="2", tab_label="check28",
        tab_group_labels=["yn9"], required="false", x_position="494", y_position="285",
    )
    check29 = Checkbox(
        document_id="1", page_number="2", tab_label="check29",
        tab_group_labels=["yn9"], required="false", x_position="544", y_position="285",
    )
    yn9 = TabGroup(
        document_id="1", page_number="2", recipient_id="1", tab_scope="Document",
        group_rule="SelectAtMost", minimum_required="0", maximum_allowed="1",
        group_label="yn9"
    )

    income10 = Text(
      document_id="1", page_number="2", x_position="281", y_position="308",
      required="false", tab_label="income10", height="12", width="60"
    )
    check30 = Checkbox(
        document_id="1", page_number="2", tab_label="check30",
        tab_group_labels=["yn10"], required="false", x_position="443", y_position="308",
    )
    check31 = Checkbox(
        document_id="1", page_number="2", tab_label="check31",
        tab_group_labels=["yn10"], required="false", x_position="494", y_position="308",
    )
    check32 = Checkbox(
        document_id="1", page_number="2", tab_label="check32",
        tab_group_labels=["yn10"], required="false", x_position="544", y_position="308",
    )
    yn10 = TabGroup(
        document_id="1", page_number="2", recipient_id="1", tab_scope="Document",
        group_rule="SelectAtMost", minimum_required="0", maximum_allowed="1",
        group_label="yn10"
    )

    income11 = Text(
      document_id="1", page_number="2", x_position="281", y_position="333",
      required="false", tab_label="income11", height="12", width="60"
    )
    check33 = Checkbox(
        document_id="1", page_number="2", tab_label="check33",
        tab_group_labels=["yn11"], required="false", x_position="443", y_position="333",
    )
    check34 = Checkbox(
        document_id="1", page_number="2", tab_label="check34",
        tab_group_labels=["yn11"], required="false", x_position="494", y_position="333",
    )
    check35 = Checkbox(
        document_id="1", page_number="2", tab_label="check35",
        tab_group_labels=["yn11"], required="false", x_position="544", y_position="333",
    )
    yn11 = TabGroup(
        document_id="1", page_number="2", recipient_id="1", tab_scope="Document",
        group_rule="SelectAtMost", minimum_required="0", maximum_allowed="1",
        group_label="yn11"
    )

    income12 = Text(
      document_id="1", page_number="2", x_position="281", y_position="357",
      required="false", tab_label="income12", height="12", width="60"
    )
    check36 = Checkbox(
        document_id="1", page_number="2", tab_label="check36",
        tab_group_labels=["yn12"], required="false", x_position="443", y_position="357",
    )
    check37 = Checkbox(
        document_id="1", page_number="2", tab_label="check37",
        tab_group_labels=["yn12"], required="false", x_position="494", y_position="357",
    )
    check38 = Checkbox(
        document_id="1", page_number="2", tab_label="check38",
        tab_group_labels=["yn12"], required="false", x_position="544", y_position="357",
    )
    yn12 = TabGroup(
        document_id="1", page_number="2", recipient_id="1", tab_scope="Document",
        group_rule="SelectAtMost", minimum_required="0", maximum_allowed="1",
        group_label="yn12"
    )

    income13 = Text(
      document_id="1", page_number="2", x_position="281", y_position="381",
      required="false", tab_label="income13", height="12", width="60"
    )
    check39 = Checkbox(
        document_id="1", page_number="2", tab_label="check39",
        tab_group_labels=["yn13"], required="false", x_position="443", y_position="381",
    )
    check40 = Checkbox(
        document_id="1", page_number="2", tab_label="check40",
        tab_group_labels=["yn13"], required="false", x_position="494", y_position="381",
    )
    check41 = Checkbox(
        document_id="1", page_number="2", tab_label="check41",
        tab_group_labels=["yn13"], required="false", x_position="544", y_position="381",
    )
    yn13 = TabGroup(
        document_id="1", page_number="2", recipient_id="1", tab_scope="Document",
        group_rule="SelectAtMost", minimum_required="0", maximum_allowed="1",
        group_label="yn13"
    )

    income_total = Text(
      document_id="1", page_number="2", x_position="281", y_position="405",
      required="false", tab_label="income13", height="12", width="60"
    )
    check42 = Checkbox(
        document_id="1", page_number="2", tab_label="check42",
        tab_group_labels=["yn14"], required="false", x_position="443", y_position="405",
    )
    check43 = Checkbox(
        document_id="1", page_number="2", tab_label="check43",
        tab_group_labels=["yn14"], required="false", x_position="494", y_position="405",
    )
    check44 = Checkbox(
        document_id="1", page_number="2", tab_label="check44",
        tab_group_labels=["yn14"], required="false", x_position="544", y_position="405",
    )
    yn14 = TabGroup(
        document_id="1", page_number="2", recipient_id="1", tab_scope="Document",
        group_rule="SelectAtMost", minimum_required="1", maximum_allowed="1",
        group_label="yn14"
    )

    last_12 = Text(
        document_id="1", page_number="1", x_position="154", y_position="657",
        required="true", tab_label="last_12", height="12", width="80"
    )

    attachment = SignerAttachment(
        document_id="1", page_number="2", x_position="40", y_position="634",
        optional='true'
    )

    sign_here = SignHere(
        document_id="1", page_number="2", x_position="102", y_position="576"
    )

    date_signed = DateSigned(
        document_id="1", page_number="2", x_position="456", y_position="587"
    )

    if args.get("useWithoutExtension", False):
        phone, address_tabs, ssn = make_tabs_without_extensions()
        print("Not using extensions")
    else:
        phone, address_tabs, ssn = make_tabs_with_extensions(session)
        print("Using extensions")

    # The Tabs object requires arrays of the different field/tab types
    signer.tabs = Tabs(
        text_tabs=[last_name, first_name, ssn, individual_assets, family_assets, asset1, asset2, asset3,
        asset4, asset5, asset6, asset_total, last_12, income1, income2,
        income3, income4, income5, income6, income7, income8, income9,
        income10, income11, income12, income13, income_total, phone, *address_tabs],
        number_tabs=[family_size],
        checkbox_tabs=[
            check1, check2, check3, check4, check5, check6,
            check7, check8, check9,
            check10, check11, check12, check13, check14,
            check15, check16, check17, check18, check19,
            check20, check21, check22, check23, check24,
            check25, check26, check27, check28, check29,
            check30, check31, check32, check33, check34,
            check35, check36, check37, check38, check39,
            check40, check41,check42, check43, check44
        ],
        tab_groups=[yn0, yn1, yn2, yn3, yn4, yn5, yn6, yn7, yn8, yn9, yn10, yn11, yn12, yn13, yn14],
        signer_attachment_tabs=[attachment],
        sign_here_tabs=[sign_here],
        date_signed_tabs=[date_signed]
    )
    return signer
