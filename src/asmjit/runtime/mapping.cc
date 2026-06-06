// ---------------------------------------------------------------------------
// \file mapping.cc
// \note Copyright (c) 2026 by Jens Kallup - paule32
//       all rights reserved.
// ---------------------------------------------------------------------------
# include "dbase2many.hpp"

LabelMapping::LabelMapping(
    const std::string& asmjit,
    const std::string& target)
    :
    asmjitLabel(asmjit),
    targetLabel(target) {}

SymbolMapping::SymbolMapping(
    const std::string& address,
    const std::string& symbol)
    :
    addressText(address),
    symbolName(symbol) {}

void
LabelMappings::add(
    const std::string& asmjitLabel,
    const std::string& targetLabel)
{
    mappings.emplace_back(
        asmjitLabel,
        targetLabel);
}

void
LabelMappings::clear() { mappings.clear(); }

void
LabelMappings::remove(const std::string& asmjitLabel)
{
    mappings.erase(
    std::remove_if(
        mappings.begin(),
        mappings.end(),
        [&](const LabelMapping& item)
        {
            return item.asmjitLabel == asmjitLabel;
        }),
    mappings.end());
}

void
LabelMappings::apply(std::string& asm_text)
{
    for (const auto& item : mappings)
    {
        replace_all(
            asm_text,
            item.asmjitLabel + ":",
            item.targetLabel + ":");

        replace_all(
            asm_text,
            item.asmjitLabel,
            item.targetLabel);
    }
}

void
SymbolMappings::add(
    const std::string& addressText,
    const std::string& symbolName) {
    
    mappings.emplace_back(addressText, symbolName);
}

void
SymbolMappings::apply(
    std::string& asm_text)
{
    for (const auto& item : mappings)
    {
        replace_all(
            asm_text,
            item.addressText,
            item.symbolName);
    }
}
