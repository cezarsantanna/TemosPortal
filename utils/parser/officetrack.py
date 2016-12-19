# -*- coding: utf-8 -*-
import psycopg2.extensions
from base64 import b64decode
from datetime import datetime
from lxml import etree


def getEventType(_xml):
    EventType = _xml.find('EventType')
    if EventType is not None:
        return EventType.text
    else:
        return None


def getEntryType(_xml):
    EntryType = _xml.find('EntryType')
    if EntryType is not None:
        return EntryType.text
    else:
        return None


def getEntryDate(_xml):
    EntryDate = _xml.find('EntryDateFromEpoch')
    if EntryDate is not None:
        return EntryDate.text[0:10]
    else:
        return None


def getEmployeeName(_xml):
    EmployeeName = _xml.find('Employee/FirstName')
    if EmployeeName is not None:
        return EmployeeName.text
    else:
        return None


def getFormName(_xml):
    if getEntryType(_xml) == '60':
        FormName = _xml.find('Form/Name')
        if FormName is not None:
            return FormName.text
        else:
            return None
    elif getEntryType(_xml) == '26':
        FormName = _xml.find('Task/TaskType/Name')
        if FormName is not None:
            return FormName.text
        else:
            return None


def getEventNumber(_xml):
    if getEntryType(_xml) == '60':
        for element in _xml.iter("Field"):
            if element[0].text == 'NÚMERO DE CHAMADO' or element[
                    0].text == 'NÚMERO DO CHAMADO':
                return element[1].text.replace(" ", "")
        return None
    elif getEntryType(_xml) == '26':
        EventNumber = _xml.find('Task/Description')
        if EventNumber is not None:
            return EventNumber.text.split()[0]
        else:
            return None


def getCGMPCode(_xml):
    if getEntryType(_xml) == '60':
        CGMPCode = _xml.find(
            'ReferencedPointsOfInterest/PointOfInterest/CustomerNumber')
        if CGMPCode is not None:
            return CGMPCode.text[-4:]
        else:
            return None
    elif getEntryType(_xml) == '26':
        CGMPCode = _xml.find('Task/Customer/CustomerNumber')
        if CGMPCode is not None:
            return CGMPCode.text
        else:
            return None


def getNomePosto(_xml):
    if getEntryType(_xml) == '60':
        if getCGMPCode(_xml) is not None:
            NomePosto = _xml.find(
                'ReferencedPointsOfInterest/PointOfInterest/Name')
            if NomePosto is not None:
                return NomePosto.text.strip()
            else:
                return None
        else:
            NomePosto = _xml.find('EntryLocation/Address')
            if NomePosto is not None:
                return NomePosto.text.strip()
            else:
                return None
    elif getEntryType(_xml) == '26':
        NomePosto = _xml.find('Task/Customer/Name')
        if NomePosto is not None:
            return NomePosto.text.strip()
        else:
            return None


def getEquipamentosSub(_xml):
    if getEntryType(_xml) == '60':
        for element in _xml.iter("Field"):
            if element[0].text == 'PERIFÉRICOS SUBSTITUÍDOS':
                _rows = element[1]
                rows = []
                for _row in _rows.iter("Row"):
                    equipamento = 'N/A'
                    serial_old = 'N/A'
                    serial_new = 'N/A'
                    for column in _row.iter("Field"):
                        if column[0].text == 'EQUIPAMENTO SUBSTITUÍDO':
                            equipamento = column[1].text
                        elif column[0].text == 'SERIAL EQUIPAMENTO RETIRADO':
                            serial_old = column[1].text
                        elif column[0].text == 'SERIAL EQUIPAMENTO ADICIONADO':
                            serial_new = column[1].text
                    row = {
                        'Equipamento': equipamento,
                        'SerialNew': serial_new,
                        'SerialOld': serial_old, }
                    if (equipamento != 'N/A' or
                        serial_old != 'N/A' or
                        serial_new != 'N/A'):
                        rows.append(row)
                return rows
    return None


def EventInfo(_xml, _entrytype):
    EntryDate = getEntryDate(_xml)
    EmployeeName = getEmployeeName(_xml)
    FormName = getFormName(_xml)
    EventNumber = getEventNumber(_xml)
    CGMPCode = getCGMPCode(_xml)
    NomePosto = getNomePosto(_xml)
    Equipamentos = getEquipamentosSub(_xml)
    if (EntryDate is None or
        EmployeeName is None or
        FormName is None or
        EventNumber is None or
        CGMPCode is None or
        NomePosto is None):
        return {
            'EntryType': _entrytype,
            'attach': _xml,
        }
    else:
        return {
            'EntryDate': EntryDate,
            'EmployeeName': EmployeeName,
            'FormName': FormName,
            'EventNumber': EventNumber,
            'CGMPCode': CGMPCode,
            'NomePosto': NomePosto,
            'EntryType': _entrytype,
            'Equipamentos': Equipamentos,
            'attach': _xml,
        }
        
def parserOfficeTrack(_source, _mail):
    attach = b64decode(_mail.attachments_list[0]['payload'])
    xml = etree.fromstring(attach)
    if (getEmployeeName(xml) == 'Eduardo' or 
        getEmployeeName(xml) == 'Cezar' or
        getEmployeeName(xml) == 'Engenharia E2i9 TESTE API'):
        return _source.replace('/new/', '/trash/')
        pass
    else:
        if getEntryType(xml) == '21':
            return _source.replace('/new/', '/OfficeTrack/RH/PunchIn/not_parsed/')
        elif getEntryType(xml) == '22':
            return _source.replace('/new/', '/OfficeTrack/RH/PunchOut/not_parsed/')
        elif getEntryType(xml) == '23':
            return _source.replace('/new/', '/OfficeTrack/Task/Start/not_parsed/')
        elif getEntryType(xml) == '24':
            return _source.replace('/new/', '/OfficeTrack/Task/End/not_parsed/')
        elif getEntryType(xml) == '25':
            return _source.replace('/new/', '/OfficeTrack/Task/Confirmed/not_parsed/')
        elif getEntryType(xml) == '26':
            return _source.replace('/new/', '/OfficeTrack/Task/Close/not_parsed/')
        elif getEntryType(xml) == '29':
            return _source.replace('/new/', '/OfficeTrack/Task/NotDone/not_parsed/')
        elif getEntryType(xml) == '60':
            return _source.replace('/new/', '/OfficeTrack/Reports/not_parsed/')
        else:
            return _source.replace('/new/', '/Others/not_parsed/')